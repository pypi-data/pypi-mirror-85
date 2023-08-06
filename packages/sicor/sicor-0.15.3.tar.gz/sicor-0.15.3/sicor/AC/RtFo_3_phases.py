#!/usr/bin/env python
# coding: utf-8

# SICOR is a freely available, platform-independent software designed to process hyperspectral remote sensing data,
# and particularly developed to handle data from the EnMAP sensor.

# This file contains the radiative transfer forward operator including a three phases of water retrieval.

# Copyright (C) 2018  Niklas Bohn (GFZ, <nbohn@gfz-potsdam.de>),
# German Research Centre for Geosciences (GFZ, <https://www.gfz-potsdam.de>)

# This software was developed within the context of the EnMAP project supported by the DLR Space Administration with
# funds of the German Federal Ministry of Economic Affairs and Energy (on the basis of a decision by the German
# Bundestag: 50 EE 1529) and contributions from DLR, GFZ and OHB System AG.

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
# version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.


import logging
import numpy as np
import pandas as pd
import dill
from multiprocessing import Pool
from itertools import product
from time import time
import warnings
from contextlib import closing
from tqdm import tqdm
import os
import pkgutil
import platform
import urllib.request

from py_tools_ds.processing.progress_mon import ProgressBar

from sicor.Tools.EnMAP.metadata import varsol
from sicor.Tools.EnMAP.LUT import get_data_file, read_lut_enmap_formatted, interpol_lut_c
from sicor.Tools.EnMAP.conversion import generate_filter, table_to_array
from sicor.Tools.EnMAP.optimal_estimation import invert_function
from sicor.Tools.EnMAP.multiprocessing import SharedNdarray, initializer, mp_progress_bar
from sicor.Tools.EnMAP.segmentation import SLIC_segmentation


# Generic
class FoGen(object):
    """
    Forward operator for input TOA radiance data formatted according to options file
    (i.e., not in standard EnMAP L1B format).
    """
    def __init__(self, data, options, logger=None):
        """
        Instance of forward operator object.

        :param data:    ndarray containing data
        :param options: dictionary with EnMAP specific options
        :param logger:  None or logging instance
        """
        self.logger = logger or logging.getLogger(__name__)
        self.cpu = options["EnMAP"]["Retrieval"]["cpu"]
        self.instrument = options["sensor"]["name"]
        self.data = data

        # get observation metadata
        self.logger.info("get observation metadata...")
        self.dsol = varsol(jday=options["sensor"]["metadata"]["jday"], month=options["sensor"]["metadata"]["month"])
        self.dn2rad = self.dsol * self.dsol * 0.1
        self.fac = 1 / self.dn2rad

        self.sza = np.full(self.data.shape[:2], options["sensor"]["metadata"]["sza"])
        self.vza = np.full(self.data.shape[:2], options["sensor"]["metadata"]["vza"])
        self.hsf = np.full(self.data.shape[:2], options["sensor"]["metadata"]["hsf"])

        # TODO: implement aot retrieval

        self.saa = np.zeros(np.full(self.data.shape[:2], options["sensor"]["metadata"]["saa"]).shape)
        for ii in range(self.saa.shape[0]):
            for jj in range(self.saa.shape[1]):
                if np.full(self.data.shape[:2], options["sensor"]["metadata"]["saa"])[ii, jj] < 0:
                    self.saa[ii, jj] = 360 + np.full(self.data.shape[:2],
                                                     options["sensor"]["metadata"]["saa"])[ii, jj]
                else:
                    self.saa[ii, jj] = np.full(self.data.shape[:2],
                                               options["sensor"]["metadata"]["saa"])[ii, jj]
        self.raa = np.abs(np.full(self.data.shape[:2],
                                  options["sensor"]["metadata"]["vza"]) - self.saa)
        for ii in range(self.raa.shape[0]):
            for jj in range(self.raa.shape[1]):
                if self.raa[ii, jj] > 180:
                    self.raa[ii, jj] = 360 - self.raa[ii, jj]

        # check if observation metadata values are within LUT value ranges
        self.logger.info("check if observation metadata values are within LUT value ranges...")
        try:
            assert np.min(self.vza) >= 0 and np.max(self.vza) <= 40
        except AssertionError:
            raise AssertionError("vza not in LUT range, must be between 0 and 40. check input value!")

        try:
            assert np.min(self.sza) >= 0 and np.max(self.sza) <= 70
        except AssertionError:
            raise AssertionError("sza not in LUT range, must be between 0 and 70. check input value!")

        try:
            assert np.min(self.hsf) >= 0 and np.max(self.hsf) <= 8
        except AssertionError:
            raise AssertionError("surface elevation not in LUT range, must be between 0 and 8. check input value!")

        try:
            assert 0.05 <= options["sensor"]["metadata"]["aot"] <= 0.8
        except AssertionError:
            raise AssertionError("aot not in LUT range, must be between 0.05 and 0.8. check input value!")

        self.pt = np.zeros((self.data.shape[0], self.data.shape[1], 5))
        self.pt[:, :, 0] = self.vza
        self.pt[:, :, 1] = self.sza
        self.pt[:, :, 2] = self.hsf
        self.pt[:, :, 3] = np.full(self.data.shape[:2], options["sensor"]["metadata"]["aot"])
        self.pt[:, :, 4] = self.raa

        if options["EnMAP"]["Retrieval"]["ice"]:
            self.ice = True
            self.par_opt = ["cwv", "a", "b", "dw", "di"]
        else:
            self.ice = False
            self.par_opt = ["cwv", "a", "b", "dw"]

        # wvl
        self.wvl = np.array(options["sensor"]["spectral"]["wvl_center"])
        self.fwhm = np.array(options["sensor"]["spectral"]["fwhm"])

        # fit wvl
        self.fit_wvl = np.array(options["FO_settings"]["fit_wvl"])
        self.wvl_sel = self.wvl[self.fit_wvl]
        self.fwhm_sel = self.fwhm[self.fit_wvl]
        self.snr_fit = np.array(options["sensor"]["spectral"]["snr"])

        # get solar irradiances for absorption feature shoulders wavelengths
        self.logger.info("get solar irradiances for absorption feature shoulders wavelengths...")
        new_kur_fn = get_data_file(module_name="sicor", file_basename="newkur_EnMAP.dat")
        new_kur = pd.read_table(new_kur_fn, delim_whitespace=True)
        freq_0 = 10e6 / self.wvl_sel[0]
        freq_1 = 10e6 / self.wvl_sel[-1]
        solar_0 = np.zeros(1)
        solar_1 = np.zeros(1)
        for ii in range(1, new_kur.shape[0]):
            if int(freq_0) - int(new_kur.at[ii, "FREQ"]) == 0:
                solar_0 = new_kur.at[ii, "SOLAR"]
            if int(freq_1) - int(new_kur.at[ii, "FREQ"]) == 0:
                solar_1 = new_kur.at[ii, "SOLAR"]

        self.s0 = float(solar_0) * (10e6 / self.wvl_sel[0]) ** 2
        self.s1 = float(solar_1) * (10e6 / self.wvl_sel[-1]) ** 2

        # load RT LUT
        self.logger.info("load RT LUT...")
        if os.path.isfile(options["retrieval"]["fn_LUT"]):
            self.fn_table = options["retrieval"]["fn_LUT"]
        else:
            self.path_sicorlib = os.path.dirname(pkgutil.get_loader("sicor").path)
            self.path_LUT_default = os.path.join(self.path_sicorlib, "AC", "data", "EnMAP_LUT_MOD5_formatted_1nm")
            if os.path.isfile(self.path_LUT_default):
                self.fn_table = self.path_LUT_default
            else:
                self.logger.info("LUT file was not found locally. Try to download it from Git repository...")
                self.fname =\
                    "https://gitext.gfz-potsdam.de/EnMAP/sicor/-/raw/master/sicor/AC/data/EnMAP_LUT_MOD5_formatted_1nm"
                urllib.request.urlretrieve(self.fname, self.path_LUT_default)
                if os.path.isfile(self.path_LUT_default):
                    self.fn_table = self.path_LUT_default
                else:
                    raise FileNotFoundError('Download of LUT file failed. Please download it manually from'
                                            'https://gitext.gfz-potsdam.de/EnMAP/sicor and store it at /sicor/AC/data/'
                                            'directory. Otherwise, the AC will not work.')

        # fn_table = get_data_file(module_name="sicor", file_basename="EnMAP_LUT_MOD5_formatted_1nm")
        luts, axes_x, axes_y, wvl, lut1, lut2, xnodes, nm_nodes, ndim, x_cell = read_lut_enmap_formatted(
            file_lut=self.fn_table)

        self.wvl_lut = wvl

        # resampling LUT to instrument wavelengths
        self.logger.info("resampling LUT to instrument wavelengths...")

        self.s_norm_fit = generate_filter(wvl_m=self.wvl_lut, wvl=self.wvl_sel, wl_resol=self.fwhm_sel)
        self.s_norm_full = generate_filter(wvl_m=self.wvl_lut, wvl=self.wvl, wl_resol=self.fwhm)

        self.xnodes = xnodes
        self.nm_nodes = nm_nodes
        self.ndim = ndim
        self.x_cell = x_cell

        lut2_all_res_fit = np.zeros((5, 6, 4, 6, 1, 7, len(self.wvl_sel), 4))
        lut2_all_res_full = np.zeros((5, 6, 4, 6, 1, 7, len(self.wvl), 4))

        lut1_res_fit = lut1[:, :, :, :, :, :, :, 0] @ self.s_norm_fit
        lut1_res_full = lut1[:, :, :, :, :, :, :, 0] @ self.s_norm_full
        for ii in range(4):
            lut2_all_res_fit[:, :, :, :, :, :, :, ii] = lut2[:, :, :, :, :, :, :, ii] @ self.s_norm_fit
            lut2_all_res_full[:, :, :, :, :, :, :, ii] = lut2[:, :, :, :, :, :, :, ii] @ self.s_norm_full

        self.lut1_fit = lut1_res_fit
        self.lut1_full = lut1_res_full
        self.lut2_fit = lut2_all_res_fit
        self.lut2_full = lut2_all_res_full

        # load imaginary parts of refractive indexes of liquid water and ice
        self.logger.info("load imaginary parts of refractive indexes of liquid water and ice...")
        path_k = get_data_file(module_name="sicor", file_basename="k_liquid_water_ice.xlsx")
        k_wi = pd.read_excel(io=path_k)
        wvl_water, k_water = table_to_array(k_wi=k_wi, a=0, b=982, col_wvl="wvl_6", col_k="T = 20°C")
        interp_kw = np.interp(x=self.wvl_sel, xp=wvl_water, fp=k_water)
        self.kw = interp_kw
        if self.ice:
            wvl_ice, k_ice = table_to_array(k_wi=k_wi, a=0, b=135, col_wvl="wvl_4", col_k="T = -7°C")
            interp_ki = np.interp(x=self.wvl_sel, xp=wvl_ice, fp=k_ice)
            self.ki = interp_ki

        # load mean solar exoatmospheric irradiances
        self.logger.info("load mean solar exoatmospheric irradiances...")
        path_sol = get_data_file(module_name="sicor", file_basename="solar_irradiances_400_2500_1.dill")
        with open(path_sol, "rb") as fl:
            solar_lut = dill.load(fl)
        self.solar_res = solar_lut @ self.s_norm_fit

    def rho_beer_lambert(self, xx):
        """
        Nonlinear surface reflectance model using the Beer-Lambert attenuation law for the retrieval of liquid water and
        ice path lengths.

        :param xx: state vector
        :return:   modeled surface reflectance
        """
        # modeling of surface reflectance
        if self.ice:
            rho = (xx[1] + (xx[2] * self.wvl_sel)) * np.exp((-xx[3] * 1e7 * ((4 * np.pi * self.kw) / self.wvl_sel)) -
                                                            (xx[4] * 1e7 * ((4 * np.pi * self.ki) / self.wvl_sel)))
        else:
            rho = (xx[1] + (xx[2] * self.wvl_sel)) * np.exp((-xx[3] * 1e7 * ((4 * np.pi * self.kw) / self.wvl_sel)))

        return rho

    def toa_rad(self, xx, pt):
        """
        Model TOA radiance for a given atmospheric state by interpolating in the LUT and applying the simplified
        solution of the RTE. Here, the atmospheric state also contains path lengths of liquid water and ice. The needed
        surface reflectance values are derived from the nonlinear Beer-Lambert surface reflectance model.

        :param xx: state vector
        :param pt: model parameter vector
        :return:   modeled TOA radiance, modeled surface reflectance
        """
        # LUT interpolation
        vtest = np.asarray([pt[0], pt[1], pt[2], pt[3], pt[4], xx[0]])
        f_int = interpol_lut_c(lut1=self.lut1_fit, lut2=self.lut2_fit, xnodes=self.xnodes, nm_nodes=self.nm_nodes,
                               ndim=self.ndim, x_cell=self.x_cell, vtest=vtest, intp_wvl=self.wvl_sel)

        f_int_l0 = f_int[0, :] * 1.e+3
        f_int_edir = f_int[1, :] * 1.e+3
        f_int_edif = f_int[2, :] * 1.e+3
        f_int_ss = f_int[3, :]

        f_int_ee = f_int_edir * np.cos(np.deg2rad(pt[1])) + f_int_edif

        # modeling of surface reflectance
        rho = self.rho_beer_lambert(xx=xx)

        # modeling of TOA radiance
        f_int_toa = (f_int_l0 + f_int_ee * rho / np.pi / (1 - f_int_ss * rho)) * self.fac

        return f_int_toa

    def surf_ref(self, dt, xx, pt, mode=None):
        """
        Model surface reflectance for a given atmospheric state by interpolating in the LUT and applying the simplified
        solution of the RTE. Here, the atmospheric state also contains path lengths of liquid water and ice.

        :param dt:   measurement vector
        :param xx:   state vector
        :param pt:   model parameter vector
        :param mode: if vnir, interpolation is done for EnMAP vnir bands; if swir, it is done for swir bands
        :return:     modeled surface reflectance
        """
        # LUT interpolation
        vtest = np.asarray([pt[0], pt[1], pt[2], pt[3], pt[4], xx[0]])

        if mode == "full":
            f_int = interpol_lut_c(lut1=self.lut1_full, lut2=self.lut2_full, xnodes=self.xnodes, nm_nodes=self.nm_nodes,
                                   ndim=self.ndim, x_cell=self.x_cell, vtest=vtest, intp_wvl=self.wvl)
        else:
            f_int = interpol_lut_c(lut1=self.lut1_fit, lut2=self.lut2_fit, xnodes=self.xnodes, nm_nodes=self.nm_nodes,
                                   ndim=self.ndim, x_cell=self.x_cell, vtest=vtest, intp_wvl=self.wvl_sel)

        f_int_l0 = f_int[0, :] * 1.e+3 * self.fac
        f_int_edir = f_int[1, :] * 1.e+3 * self.fac
        f_int_edif = f_int[2, :] * 1.e+3 * self.fac
        f_int_ss = f_int[3, :]

        f_int_ee = f_int_edir * np.cos(np.deg2rad(pt[1])) + f_int_edif

        # modeling of surface reflectance
        xterm = np.pi * (dt - f_int_l0) / f_int_ee
        rho = xterm / (1. + f_int_ss * xterm)

        return rho


# EnMAP
class Fo(object):
    """
    Forward operator for input TOA radiance data in standard EnMAP L1B format.
    """
    def __init__(self, enmap_l1b, options, logger=None):
        """
        Instance of forward operator object.

        :param enmap_l1b: EnMAP Level-1B object
        :param options:   dictionary with EnMAP specific options
        :param logger:    None or logging instance
        """
        self.logger = logger or logging.getLogger(__name__)
        self.cpu = options["EnMAP"]["Retrieval"]["cpu"]
        self.disable_progressbars = options["EnMAP"]["Retrieval"]["disable_progressbars"]
        self.instrument = "EnMAP"
        self.data = enmap_l1b.swir.data
        self.data_fg = enmap_l1b.vnir.data
        self.enmap_rad_all = np.concatenate((self.data_fg, self.data), axis=2)

        # get observation metadata
        self.logger.info("Getting observation metadata...")
        self.jday = enmap_l1b.meta.observation_datetime.day
        self.month = enmap_l1b.meta.observation_datetime.month
        self.dsol = varsol(jday=self.jday, month=self.month)
        self.dn2rad = self.dsol * self.dsol * 0.1
        self.fac = 1 / self.dn2rad

        self.sza = np.full(enmap_l1b.swir.data.shape[:2], enmap_l1b.meta.geom_sun_zenith)

        self.raa = np.zeros(enmap_l1b.swir.data.shape[:2])

        if enmap_l1b.meta.geom_sun_azimuth < 0:
            self.saa = 360 + enmap_l1b.meta.geom_sun_azimuth
        else:
            self.saa = enmap_l1b.meta.geom_sun_azimuth

        self.geom_rel_azimuth = np.abs(enmap_l1b.meta.geom_view_zenith - self.saa)
        if self.geom_rel_azimuth > 180:
            self.raa[:, :] = 360 - self.geom_rel_azimuth
        else:
            self.raa[:, :] = self.geom_rel_azimuth

        # get dem for each detector, if no dem is provided by the L1B object the algorithm falls back to an average
        # elevation given in the EnPT config file
        self.hsf = {}
        for detector_name in enmap_l1b.detector_attrNames:
            detector = getattr(enmap_l1b, detector_name)
            if detector.dem.size == 0:
                self.hsf[detector_name] = np.full(detector.data.shape[:2], (enmap_l1b.cfg.average_elevation / 1000))
            else:
                self.hsf[detector_name] = detector.dem[:, :] / 1000

        # check if observation metadata values are within LUT value ranges
        self.logger.info("Checking if observation metadata values are within LUT value ranges...")
        try:
            assert 0 <= enmap_l1b.meta.geom_view_zenith <= 40
        except AssertionError:
            raise AssertionError("vza not in LUT range, must be between 0 and 40. check input value!")

        try:
            assert np.min(self.sza) >= 0 and np.max(self.sza) <= 70
        except AssertionError:
            raise AssertionError("sza not in LUT range, must be between 0 and 70. check input value!")

        try:
            assert np.min(self.hsf["swir"]) >= 0 and np.max(self.hsf["swir"]) <= 8
        except AssertionError:
            raise AssertionError("surface elevation not in LUT range, must be between 0 and 8. check input value!")

        try:
            assert 0.05 <= options["EnMAP"]["FO_settings"]["aot"] <= 0.8
        except AssertionError:
            raise AssertionError("aot not in LUT range, must be between 0.05 and 0.8. check input value!")

        self.pt = np.zeros((self.data.shape[0], self.data.shape[1], 5))
        self.pt[:, :, 0] = np.full(enmap_l1b.swir.data.shape[:2], enmap_l1b.meta.geom_view_zenith)
        self.pt[:, :, 1] = self.sza
        self.pt[:, :, 2] = self.hsf["swir"]
        self.pt[:, :, 3] = np.full(enmap_l1b.swir.data.shape[:2], options["EnMAP"]["FO_settings"]["aot"])
        self.pt[:, :, 4] = self.raa

        if options["EnMAP"]["Retrieval"]["ice"]:
            self.ice = True
            self.par_opt = ["cwv", "a", "b", "dw", "di"]
        else:
            self.ice = False
            self.par_opt = ["cwv", "a", "b", "dw"]

        # fit wvl
        self.fit_wvl = np.array([14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31])
        self.wvl_sel = np.array(enmap_l1b.swir.detector_meta.wvl_center[self.fit_wvl])
        self.fwhm_sel = np.array(enmap_l1b.swir.detector_meta.fwhm[self.fit_wvl])
        self.snr_fit = np.array([322.94254006, 313.45752342, 313.32464722, 306.19455173, 281.35641378, 227.9759974,
                                 157.22390595, 148.93620623, 154.40197388, 182.60431866, 232.89644996,
                                 250.1244036, 252.2267179, 272.16592448, 299.71964816, 316.11909184, 326.33202741,
                                 312.28461288])

        # vnir wvl
        self.wvl_vnir = np.array(enmap_l1b.vnir.detector_meta.wvl_center[:])
        self.fwhm_vnir = np.array(enmap_l1b.vnir.detector_meta.fwhm[:])

        # swir wvl
        self.wvl_swir = np.array(enmap_l1b.swir.detector_meta.wvl_center[:])
        self.fwhm_swir = np.array(enmap_l1b.swir.detector_meta.fwhm[:])

        self.enmap_wvl_all = np.concatenate((self.wvl_vnir, self.wvl_swir))
        self.enmap_fwhm_all = np.concatenate((self.fwhm_vnir, self.fwhm_swir))

        # get solar irradiances for absorption feature shoulders wavelengths
        self.logger.info("Getting solar irradiances for absorption feature shoulders wavelengths...")
        new_kur_fn = get_data_file(module_name="sicor", file_basename="newkur_EnMAP.dat")
        new_kur = pd.read_csv(new_kur_fn, delim_whitespace=True)
        freq_0 = 10e6 / self.wvl_sel[0]
        freq_1 = 10e6 / self.wvl_sel[-1]
        solar_0 = np.zeros(1)
        solar_1 = np.zeros(1)
        for ii in range(1, new_kur.shape[0]):
            if int(freq_0) - int(new_kur.at[ii, "FREQ"]) == 0:
                solar_0 = new_kur.at[ii, "SOLAR"]
            if int(freq_1) - int(new_kur.at[ii, "FREQ"]) == 0:
                solar_1 = new_kur.at[ii, "SOLAR"]

        self.s0 = float(solar_0) * (10e6 / self.wvl_sel[0]) ** 2
        self.s1 = float(solar_1) * (10e6 / self.wvl_sel[-1]) ** 2

        # load RT LUT
        # check if LUT file is available
        self.logger.info("Loading RT LUT...")
        if os.path.isfile(options["EnMAP"]["Retrieval"]["fn_LUT"]):
            self.fn_table = options["EnMAP"]["Retrieval"]["fn_LUT"]
        else:
            self.path_sicorlib = os.path.dirname(pkgutil.get_loader("sicor").path)
            self.path_LUT_default = os.path.join(self.path_sicorlib, "AC", "data", "EnMAP_LUT_MOD5_formatted_1nm")
            if os.path.isfile(self.path_LUT_default):
                self.fn_table = self.path_LUT_default
            else:
                self.logger.info("LUT file was not found locally. Try to download it from Git repository...")
                self.fname = \
                    "https://gitext.gfz-potsdam.de/EnMAP/sicor/-/raw/master/sicor/AC/data/EnMAP_LUT_MOD5_formatted_1nm"
                urllib.request.urlretrieve(self.fname, self.path_LUT_default)
                if os.path.isfile(self.path_LUT_default):
                    self.fn_table = self.path_LUT_default
                else:
                    raise FileNotFoundError('Download of LUT file failed. Please download it manually from'
                                            'https://gitext.gfz-potsdam.de/EnMAP/sicor and store it at /sicor/AC/data/'
                                            'directory. Otherwise, the AC will not work.')

        # check if LUT is a regular file (not only an LFS pointer)
        try:
            assert os.path.getsize(self.fn_table) > 1000
            self.logger.info("LUT file was properly downloaded and is available for AC!")
        except AssertionError:
            raise AssertionError("LUT file only represents an LFS pointer. Make sure to download the file following "
                                 "the installation documentation on Git. Otherwise, the AC will not work.")

        luts, axes_x, axes_y, wvl, lut1, lut2, xnodes, nm_nodes, ndim, x_cell = read_lut_enmap_formatted(
            file_lut=self.fn_table)

        self.wvl = wvl
        self.xnodes = xnodes
        self.nm_nodes = nm_nodes
        self.ndim = ndim
        self.x_cell = x_cell

        # resampling LUT to EnMAP wavelengths
        self.logger.info("Resampling LUT to EnMAP wavelengths...")

        self.s_norm_fit = generate_filter(wvl_m=self.wvl, wvl=self.wvl_sel, wl_resol=self.fwhm_sel)
        self.s_norm_vnir = generate_filter(wvl_m=self.wvl, wvl=self.wvl_vnir, wl_resol=self.fwhm_vnir)
        self.s_norm_swir = generate_filter(wvl_m=self.wvl, wvl=self.wvl_swir, wl_resol=self.fwhm_swir)

        lut2_all_res_fit = np.zeros((5, 6, 4, 6, 1, 7, len(self.wvl_sel), 4))
        lut2_all_res_vnir = np.zeros((5, 6, 4, 6, 1, 7, len(self.wvl_vnir), 4))
        lut2_all_res_swir = np.zeros((5, 6, 4, 6, 1, 7, len(self.wvl_swir), 4))

        lut1_res_fit = lut1[:, :, :, :, :, :, :, 0] @ self.s_norm_fit
        lut1_res_vnir = lut1[:, :, :, :, :, :, :, 0] @ self.s_norm_vnir
        lut1_res_swir = lut1[:, :, :, :, :, :, :, 0] @ self.s_norm_swir
        for ii in range(4):
            lut2_all_res_fit[:, :, :, :, :, :, :, ii] = lut2[:, :, :, :, :, :, :, ii] @ self.s_norm_fit
            lut2_all_res_vnir[:, :, :, :, :, :, :, ii] = lut2[:, :, :, :, :, :, :, ii] @ self.s_norm_vnir
            lut2_all_res_swir[:, :, :, :, :, :, :, ii] = lut2[:, :, :, :, :, :, :, ii] @ self.s_norm_swir

        self.lut1_fit = lut1_res_fit
        self.lut1_vnir = lut1_res_vnir
        self.lut1_swir = lut1_res_swir
        self.lut2_fit = lut2_all_res_fit
        self.lut2_vnir = lut2_all_res_vnir
        self.lut2_swir = lut2_all_res_swir

        # load imaginary parts of refractive indexes of liquid water and ice
        warnings.filterwarnings("ignore")
        self.logger.info("Loading imaginary parts of refractive indexes of liquid water and ice...")
        path_k = get_data_file(module_name="sicor", file_basename="k_liquid_water_ice.xlsx")
        k_wi = pd.read_excel(io=path_k)
        wvl_water, k_water = table_to_array(k_wi=k_wi, a=0, b=982, col_wvl="wvl_6", col_k="T = 20°C")
        interp_kw = np.interp(x=self.wvl_sel, xp=wvl_water, fp=k_water)
        self.kw = interp_kw
        if self.ice:
            wvl_ice, k_ice = table_to_array(k_wi=k_wi, a=0, b=135, col_wvl="wvl_4", col_k="T = -7°C")
            interp_ki = np.interp(x=self.wvl_sel, xp=wvl_ice, fp=k_ice)
            self.ki = interp_ki

        # calculate mean solar exoatmospheric irradiances
        self.logger.info("Calculating mean solar exoatmospheric irradiances...")
        path_sol = get_data_file(module_name="sicor", file_basename="solar_irradiances_400_2500_1.dill")
        with open(path_sol, "rb") as fl:
            solar_lut = dill.load(fl)
        self.solar_res = solar_lut @ self.s_norm_fit

        # do optional image segmentation to enhance processing speed
        self.segmentation = options["EnMAP"]["Retrieval"]["segmentation"]
        self.n_pca = options["EnMAP"]["Retrieval"]["n_pca"]
        self.segs = options["EnMAP"]["Retrieval"]["segs"]
        if self.segmentation:
            self.logger.info("Segmenting L1B spectra to enhance processing speed...")
            self.X, self.segs, self.labels = SLIC_segmentation(data_rad_all=self.enmap_rad_all, n_pca=self.n_pca,
                                                               segs=self.segs)

            # prepare segmented L1B data cube
            self.logger.info("Preparing segmented L1B data cube...")
            self.rdn_subset = np.zeros((1, self.segs, self.enmap_rad_all.shape[2]))
            self.dem_subset = np.zeros((1, self.segs))
            self.pt_subset = np.zeros((1, self.segs, 5))
            for i in range(self.segs):
                radiance = self.X[self.labels.flat == i, :].mean(axis=0)
                hsf_mean = self.hsf["swir"].flatten()[self.labels.flat == i].mean(axis=0)
                pt_mean = self.pt.reshape(self.pt.shape[0] * self.pt.shape[1], 5)[self.labels.flat == i, :].mean(axis=0)
                self.rdn_subset[:, i, :] = radiance
                self.dem_subset[:, i] = hsf_mean
                self.pt_subset[:, i, :] = pt_mean

    def rho_beer_lambert(self, xx):
        """
        Nonlinear surface reflectance model using the Beer-Lambert attenuation law for the retrieval of liquid water and
        ice path lengths.

        :param xx: state vector
        :return:   modeled surface reflectance
        """
        # modeling of surface reflectance
        if self.ice:
            rho = (xx[1] + (xx[2] * self.wvl_sel)) * np.exp((-xx[3] * 1e7 * ((4 * np.pi * self.kw) / self.wvl_sel)) -
                                                            (xx[4] * 1e7 * ((4 * np.pi * self.ki) / self.wvl_sel)))
        else:
            rho = (xx[1] + (xx[2] * self.wvl_sel)) * np.exp((-xx[3] * 1e7 * ((4 * np.pi * self.kw) / self.wvl_sel)))

        return rho

    def toa_rad(self, xx, pt):
        """
        Model TOA radiance for a given atmospheric state by interpolating in the LUT and applying the simplified
        solution of the RTE. Here, the atmospheric state also contains path lengths of liquid water and ice. The needed
        surface reflectance values are derived from the nonlinear Beer-Lambert surface reflectance model.

        :param xx: state vector
        :param pt: model parameter vector
        :return:   modeled TOA radiance, modeled surface reflectance
        """
        # LUT interpolation
        vtest = np.asarray([pt[0], pt[1], pt[2], pt[3], pt[4], xx[0]])
        f_int = interpol_lut_c(lut1=self.lut1_fit, lut2=self.lut2_fit, xnodes=self.xnodes, nm_nodes=self.nm_nodes,
                               ndim=self.ndim, x_cell=self.x_cell, vtest=vtest, intp_wvl=self.wvl_sel)

        f_int_l0 = f_int[0, :] * 1.e+3
        f_int_edir = f_int[1, :] * 1.e+3
        f_int_edif = f_int[2, :] * 1.e+3
        f_int_ss = f_int[3, :]

        f_int_ee = f_int_edir * np.cos(np.deg2rad(pt[1])) + f_int_edif

        # modeling of surface reflectance
        rho = self.rho_beer_lambert(xx=xx)

        # modeling of TOA radiance
        f_int_toa = (f_int_l0 + f_int_ee * rho / np.pi / (1 - f_int_ss * rho)) * self.fac

        return f_int_toa

    def surf_ref(self, dt, xx, pt, mode=None):
        """
        Model surface reflectance for a given atmospheric state by interpolating in the LUT and applying the simplified
        solution of the RTE. Here, the atmospheric state also contains path lengths of liquid water and ice.

        :param dt:   measurement vector
        :param xx:   state vector
        :param pt:   model parameter vector
        :param mode: if vnir, interpolation is done for EnMAP vnir bands; if swir, it is done for swir bands
        :return:     modeled surface reflectance
        """
        # LUT interpolation
        vtest = np.asarray([pt[0], pt[1], pt[2], pt[3], pt[4], xx[0]])
        if mode == "vnir":
            f_int = interpol_lut_c(lut1=self.lut1_vnir, lut2=self.lut2_vnir, xnodes=self.xnodes, nm_nodes=self.nm_nodes,
                                   ndim=self.ndim, x_cell=self.x_cell, vtest=vtest, intp_wvl=self.wvl_vnir)
        elif mode == "swir":
            f_int = interpol_lut_c(lut1=self.lut1_swir, lut2=self.lut2_swir, xnodes=self.xnodes, nm_nodes=self.nm_nodes,
                                   ndim=self.ndim, x_cell=self.x_cell, vtest=vtest, intp_wvl=self.wvl_swir)
        else:
            f_int = interpol_lut_c(lut1=self.lut1_fit, lut2=self.lut2_fit, xnodes=self.xnodes, nm_nodes=self.nm_nodes,
                                   ndim=self.ndim, x_cell=self.x_cell, vtest=vtest, intp_wvl=self.wvl_sel)

        f_int_l0 = f_int[0, :] * 1.e+3 * self.fac
        f_int_edir = f_int[1, :] * 1.e+3 * self.fac
        f_int_edif = f_int[2, :] * 1.e+3 * self.fac
        f_int_ss = f_int[3, :]

        f_int_ee = f_int_edir * np.cos(np.deg2rad(pt[1])) + f_int_edif

        # modeling of surface reflectance
        xterm = np.pi * (dt - f_int_l0) / f_int_ee
        rho = xterm / (1. + f_int_ss * xterm)

        return rho


class FoFunc(object):
    """
    Forward operator function function including the nonlinear Beer-Lambert model for the surface reflectance.
    """
    def __init__(self, fo):
        """
        Instance of forward operator function.

        :param fo: Forward operator
        """
        self.fo = fo

    @staticmethod
    def __norm__(aa, bb):
        """
        Calculate L2 norm between measured and modeled values.

        :param aa: measured values
        :param bb: modeled values
        :return:   L2 norm
        """
        return (aa - bb) ** 2

    @staticmethod
    def __d_bb_norm__(aa, bb):
        """
        Calculate derivative of L2 norm between measured and modeled values.

        :param aa: measured values
        :param bb: modeled values
        :return:   derivative of L2 norm
        """
        return -2 * (aa - bb)

    def __call__(self, xx, pt, dt, model_output=False):
        """
        Call forward operator function.

        :param xx:           state vector
        :param pt:           model parameter vector
        :param dt:           measurement vector
        :param model_output: if True, modeled TOA radiance and surface reflectance are returned; else, L2 norm;
                             default: False
        :return:             if model_output=False, L2 norm is returned; else, modeled TOA radiance and surface
                             reflectance
        """
        ff = self.fo.toa_rad(xx=xx, pt=pt)

        if model_output is True:
            return ff
        else:
            f = (np.sum(self.__norm__(aa=dt, bb=ff)))
            n = np.float(len(dt))

            return f / n


# noinspection PyUnresolvedReferences
def __minimize__(fo, opt_func, logger=None, oe=False, ice=False):
    """
    Minimize value of cost function using either the downhill simplex algorithm or optimal estimation.

    :param fo:       forward operator
    :param opt_func: forward operator function
    :param wv_fg:    first guess for water vapor (same dimensions like to be fitted data)
    :param logger:   None or logging instance
    :param oe:       if True, optimal estimation is used for minimization, else the downhill simplex algorithm;
                     default: False
    :param ice:      if True, liquid water and ice path lengths are retrieved; else, only liquid water; default: False
    :return:         retrieved water vapor, liquid water and ice path lengths; modeled offset and slope of absorption
                     feature linear continuum; modeled TOA radiance; if oe=False, additionally, modeled surface
                     reflectance and number of iterations are returned
    """
    logger = logger or logging.getLogger(__name__)

    # set up multiprocessing
    processes = fo.cpu
    if platform.system() == "Windows" and processes > 1:
        logger.warning("Multiprocessing is currently not available on Windows.")
    if platform.system() == "Windows" or processes == 1:
        logger.info("Singleprocessing on 1 cpu")
    else:
        logger.info("Setting up multiprocessing...")
        logger.info("Multiprocessing on %s cpu's" % processes)

    globs = dict()
    globs["__instrument__"] = fo.instrument

    if fo.segmentation:
        opt_pt = np.array(fo.pt_subset)
        opt_data = fo.rdn_subset[:, :, len(fo.wvl_vnir):][:, :, fo.fit_wvl]
        globs["__data__"] = opt_data
    else:
        opt_pt = np.array(fo.pt)
        opt_data = fo.data[:, :, fo.fit_wvl]
        globs["__data__"] = opt_data

    y1 = np.zeros((opt_data.shape[:2]))
    y2 = np.zeros((opt_data.shape[:2]))
    a = np.zeros((opt_data.shape[:2]))
    b = np.zeros((opt_data.shape[:2]))

    y1[:, :] = np.pi * opt_data[:, :, 0] / (fo.s0 * np.cos(np.deg2rad(opt_pt[:, :, 1])))
    y2[:, :] = np.pi * opt_data[:, :, -1] / (fo.s1 * np.cos(np.deg2rad(opt_pt[:, :, 1])))
    a[:, :] = y2 - ((y1 - y2) / (fo.wvl_sel[0] - fo.wvl_sel[-1])) * fo.wvl_sel[-1]
    b[:, :] = (y1 - y2) / (fo.wvl_sel[0] - fo.wvl_sel[-1])

    if ice:
        xa = np.zeros((opt_data.shape[0], opt_data.shape[1], 5))
        for ii in range(xa.shape[0]):
            for jj in range(xa.shape[1]):
                xa[ii, jj, :] = np.asarray([2.5, a[ii, jj], b[ii, jj], 0.02, 0.02], dtype=float)
    else:
        xa = np.zeros((opt_data.shape[0], opt_data.shape[1], 4))
        for ii in range(xa.shape[0]):
            for jj in range(xa.shape[1]):
                xa[ii, jj, :] = np.asarray([2.5, a[ii, jj], b[ii, jj], 0.02], dtype=float)

    globs["__xa__"] = xa

    globs["__pt__"] = opt_pt
    globs["__fit_wvl__"] = fo.fit_wvl
    globs["__s0__"] = fo.s0
    globs["__s1__"] = fo.s1
    globs["__sza__"] = opt_pt[:, :, 1]
    globs["__dsol__"] = fo.dsol
    globs["__solar_res__"] = fo.solar_res
    globs["__forward__"] = opt_func

    globs["__cwv_model__"] = SharedNdarray(dims=list(opt_data.shape[:2]))
    globs["__cwc_model__"] = SharedNdarray(dims=list(opt_data.shape[:2]))
    globs["__a_model__"] = SharedNdarray(dims=list(opt_data.shape[:2]))
    globs["__b_model__"] = SharedNdarray(dims=list(opt_data.shape[:2]))
    globs["__toa_model__"] = SharedNdarray(dims=list(opt_data.shape[:2]) + [fo.fit_wvl.shape[0]])

    if ice:
        globs["__ice_model__"] = SharedNdarray(dims=list(opt_data.shape[:2]))

    if oe:
        globs["__snr__"] = fo.snr_fit
        globs["__inv_func__"] = invert_function(fo.toa_rad)
        if ice:
            globs["__ll__"] = np.array([0.001, 0.001, -0.0004, 0.0001, 0.0001])
            globs["__ul__"] = np.array([4.999, 0.999, 0.0004, 0.499, 0.499])
            globs["__sa__"] = np.identity(5) * 1000000
            globs["__Se__"] = SharedNdarray(dims=list(opt_data.shape[:2]) + [5] + [5])
            globs["__Scem__"] = SharedNdarray(dims=list(opt_data.shape[:2]) + [5] + [5])
            globs["__Srem__"] = SharedNdarray(dims=list(opt_data.shape[:2]) + [5] + [5])
        else:
            globs["__ll__"] = np.array([0.001, 0.001, -0.0004, 0.0001])
            globs["__ul__"] = np.array([4.999, 0.999, 0.0004, 0.499])
            globs["__sa__"] = np.identity(4) * 1000000
            globs["__Se__"] = SharedNdarray(dims=list(opt_data.shape[:2]) + [4] + [4])
            globs["__Scem__"] = SharedNdarray(dims=list(opt_data.shape[:2]) + [4] + [4])
            globs["__Srem__"] = SharedNdarray(dims=list(opt_data.shape[:2]) + [4] + [4])

    if oe:
        if ice:
            mp_fun = __oe_ice__
            mp_fun_name = '3 water phases optimal estimation (vapor, liquid and ice)'
        else:
            mp_fun = __oe__
            mp_fun_name = '2 water phases optimal estimation (vapor and liquid)'
    else:
        if ice:
            mp_fun = __min_ice__
            mp_fun_name = '3 water phases downhill simplex optimization (vapor, liquid and ice)'
        else:
            mp_fun = __min__
            mp_fun_name = '2 water phases downhill simplex optimization (vapor and liquid)'

    logger.info("Inversion method: %s" % mp_fun_name)

    rng = list(product(np.arange(0, opt_data.shape[0], 1), np.arange(0, opt_data.shape[1], 1)))

    # start optimization
    logger.info("Starting optimization...")
    warnings.filterwarnings("ignore")
    t0 = time()
    # check if operating system is 'Windows'; in that case, multiprocessing is currently not working
    # TODO: enbale Windows compatibility for multiprocessing
    if platform.system() == "Windows" or processes == 1:
        initializer(globals(), globs)
        [mp_fun(ii) for ii in tqdm(rng, disable=fo.disable_progressbars)]
    else:
        with closing(Pool(processes=processes, initializer=initializer, initargs=(globals(), globs,))) as pl:
            results = pl.map_async(mp_fun, rng, chunksize=1)
            if not fo.disable_progressbars:
                bar = ProgressBar(prefix='\tprogress:')
            while True:
                if not fo.disable_progressbars:
                    mp_progress_bar(iter_list=rng, results=results, bar=bar)
                if results.ready():
                    results.get()
                    break
    t1 = time()

    cwv_model = globs["__cwv_model__"].np
    cwc_model = globs["__cwc_model__"].np
    a_model = globs["__a_model__"].np
    b_model = globs["__b_model__"].np
    toa_model = globs["__toa_model__"].np
    if ice:
        ice_model = globs["__ice_model__"].np
    else:
        ice_model = None

    if oe:
        se = globs["__Se__"].np
        scem = globs["__Scem__"].np
        srem = globs["__Srem__"].np
    else:
        se = None
        scem = None
        srem = None

    # simple validation of optimization output
    if np.sum(cwv_model - xa[:, :, 0]) == 0 or np.sum(cwc_model - xa[:, :, 3]) == 0:
        logger.warning("Optimization failed and returned first guess values. Please check for errors in the input "
                       "data, the options file, or the processing code.")
    if ice:
        if np.sum(ice_model - xa[:, :, 4]) == 0:
            logger.warning("Optimization failed and returned first guess values. Please check for errors in the input "
                           "data, the options file, or the processing code.")

    logger.info("Done!")
    logger.info("Runtime: %.2f" % (t1 - t0) + " s")

    return cwv_model, cwc_model, ice_model, a_model, b_model, toa_model, se, scem, srem


# noinspection PyUnresolvedReferences
def __min__(ii):
    """
    Minimize value of cost function using the downhill simplex algorithm.

    :param ii: index of data pixel
    """
    from scipy.optimize import minimize  # import here to avoid static TLS ImportError

    i1, i2 = ii

    ress_full = minimize(fun=__forward__, x0=__xa__[i1, i2, :], args=(__pt__[i1, i2, :], __data__[i1, i2, :]),
                         jac=False, method='Nelder-Mead', options={"disp": False})

    model = __forward__(xx=ress_full["x"], pt=__pt__[i1, i2, :], dt=__data__[i1, i2, :], model_output=True)

    __cwv_model__[i1, i2] = ress_full["x"][0]
    __cwc_model__[i1, i2] = ress_full["x"][3]
    __a_model__[i1, i2] = ress_full["x"][1]
    __b_model__[i1, i2] = ress_full["x"][2]
    __toa_model__[i1, i2] = model


# noinspection PyUnresolvedReferences
def __min_ice__(ii):
    """
    Minimize value of cost function using the downhill simplex algorithm including ice path length retrieval.

    :param ii: index of data pixel
    """
    from scipy.optimize import minimize  # import here to avoid static TLS ImportError

    i1, i2 = ii

    ress_full = minimize(fun=__forward__, x0=__xa__[i1, i2, :], args=(__pt__[i1, i2, :], __data__[i1, i2, :]),
                         jac=False, method='Nelder-Mead', options={"disp": False})

    model = __forward__(xx=ress_full["x"], pt=__pt__[i1, i2, :], dt=__data__[i1, i2, :], model_output=True)

    __cwv_model__[i1, i2] = ress_full["x"][0]
    __cwc_model__[i1, i2] = ress_full["x"][3]
    __ice_model__[i1, i2] = ress_full["x"][4]
    __a_model__[i1, i2] = ress_full["x"][1]
    __b_model__[i1, i2] = ress_full["x"][2]
    __toa_model__[i1, i2] = model


# noinspection PyUnresolvedReferences
def __oe__(ii):
    """
    Minimize value of cost function using optimal estimation.

    :param ii: index of data pixel
    """
    from scipy import sqrt  # import here to avoid static TLS ImportError

    i1, i2 = ii

    if __instrument__ == "AVIRIS":
        nedl = abs(__snr__[:, 0] * sqrt(__snr__[:, 1] + __data__[i1, i2, :]) + __snr__[:, 2])
        se = np.identity(len(__fit_wvl__)) * nedl
    else:
        se = np.identity(len(__fit_wvl__)) * ((__data__[i1, i2, :] / __snr__) ** 2)

    res = __inv_func__(yy=__data__[i1, i2, :], fparam=__pt__[i1, i2, :], ll=__ll__, ul=__ul__, xa=__xa__[i1, i2, :],
                       sa=__sa__, se=se, gnform='n', full=False, maxiter=35, eps=0.01)

    model = __forward__(xx=res[0], pt=__pt__[i1, i2, :], dt=__data__[i1, i2, :], model_output=True)

    __cwv_model__[i1, i2] = res[0][0]
    __cwc_model__[i1, i2] = res[0][3]
    __a_model__[i1, i2] = res[0][1]
    __b_model__[i1, i2] = res[0][2]
    __toa_model__[i1, i2, :] = model

    # a posteriori covariance matrix
    __Se__[i1, i2, :, :] = res[4]

    # correlation error matrix
    cem = np.zeros((4, 4))

    for mm in range(4):
        for nn in range(4):
            cem[mm, nn] = __Se__[i1, i2, :, :][mm, nn] / np.sqrt(__Se__[i1, i2, :, :][mm, mm] *
                                                                 __Se__[i1, i2, :, :][nn, nn])

    __Scem__[i1, i2, :, :] = cem

    # relative error matrix
    x_ = res[0]
    rem = np.zeros((4, 4))

    for mm in range(4):
        for nn in range(4):
            rem[mm, nn] = 100 * np.sqrt(__Se__[i1, i2, :, :][mm, nn] / (x_[mm] * x_[nn]))

    __Srem__[i1, i2, :, :] = rem


# noinspection PyUnresolvedReferences
def __oe_ice__(ii):
    """
    Minimize value of cost function using optimal estimation including ice path length retrieval.

    :param ii: index of data pixel
    """
    from scipy import sqrt  # import here to avoid static TLS ImportError

    i1, i2 = ii

    if __instrument__ == "AVIRIS":
        nedl = abs(__snr__[:, 0] * sqrt(__snr__[:, 1] + __data__[i1, i2, :]) + __snr__[:, 2])
        se = np.identity(len(__fit_wvl__)) * nedl
    else:
        se = np.identity(len(__fit_wvl__)) * ((__data__[i1, i2, :] / __snr__) ** 2)

    res = __inv_func__(yy=__data__[i1, i2, :], fparam=__pt__[i1, i2, :], ll=__ll__, ul=__ul__, xa=__xa__[i1, i2, :],
                       sa=__sa__, se=se, gnform='n', full=False, maxiter=35, eps=0.01)

    model = __forward__(xx=res[0], pt=__pt__[i1, i2, :], dt=__data__[i1, i2, :], model_output=True)

    __cwv_model__[i1, i2] = res[0][0]
    __cwc_model__[i1, i2] = res[0][3]
    __ice_model__[i1, i2] = res[0][4]
    __a_model__[i1, i2] = res[0][1]
    __b_model__[i1, i2] = res[0][2]
    __toa_model__[i1, i2, :] = model

    # a posteriori covariance matrix
    __Se__[i1, i2, :, :] = res[4]

    # correlation error matrix
    cem = np.zeros((5, 5))

    for mm in range(5):
        for nn in range(5):
            cem[mm, nn] = __Se__[i1, i2, :, :][mm, nn] / np.sqrt(__Se__[i1, i2, :, :][mm, mm] *
                                                                 __Se__[i1, i2, :, :][nn, nn])

    __Scem__[i1, i2, :, :] = cem

    # relative error matrix
    x_ = res[0]
    rem = np.zeros((5, 5))

    for mm in range(5):
        for nn in range(5):
            rem[mm, nn] = 100 * np.sqrt(__Se__[i1, i2, :, :][mm, nn] / (x_[mm] * x_[nn]))

    __Srem__[i1, i2, :, :] = rem
