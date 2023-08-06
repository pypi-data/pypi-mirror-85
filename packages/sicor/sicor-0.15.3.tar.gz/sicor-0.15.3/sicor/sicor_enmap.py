#!/usr/bin/env python
# coding: utf-8

# SICOR is a freely available, platform-independent software designed to process hyperspectral remote sensing data,
# and particularly developed to handle data from the EnMAP sensor.

# This file contains the Sensor Independent Atmospheric CORrection (SICOR) AC module - EnMAP specific parts.

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
from tqdm import tqdm
import numpy as np
import warnings

from sicor.AC.RtFo_3_phases import Fo, FoFunc, __minimize__
from sicor.Tools.EnMAP.segmentation import empirical_line_solution


def make_ac_enmap(data, enmap_l1b, fo, cwv, cwc, ice, a, b, logger=None):
    """
    Performs ac for enmap_l1b product, based on given and retrieved parameters.
    Side effect: adds 'data_l2a' attribute to each detector. This numpy array holds the surface reflectance map.

    :param data:      array containing measured TOA radiance
    :param enmap_l1b: EnMAP Level-1B object
    :param fo:        forward operator object
    :param cwv:       array containing optimized water vapor
    :param cwc:       array containing optimized liquid water
    :param ice:       array containing optimized ice
    :param a:         array containing optimized continuum slope
    :param b:         array containing optimized continuum offset
    :param logger:    None or logging instance
    :return:          None
    """
    logger = logger or logging.getLogger(__name__)

    if fo.segmentation:
        for detector_name in enmap_l1b.detector_attrNames:
            logger.info("AC for detector: %s..." % detector_name)
            detector = getattr(enmap_l1b, detector_name)
            if detector_name == "vnir":
                data_ac = data[:, :, :88]
                detector.data_l2a = np.full(data_ac.shape, np.NaN, dtype=np.float)
            else:
                data_ac = data[:, :, 88:]
                detector.data_l2a = np.full(data_ac.shape, np.NaN, dtype=np.float)
            for icol in tqdm(range(data_ac.shape[1]), disable=fo.disable_progressbars):
                for irow in range(data_ac.shape[0]):
                    detector.data_l2a[irow, icol, :] = fo.surf_ref(
                        dt=data_ac[irow, icol, :],
                        xx=np.array([cwv[irow, icol], a[irow, icol], b[irow, icol], cwc[irow, icol]]),
                        pt=fo.pt_subset[irow, icol, :], mode=detector_name)
    else:
        for detector_name in enmap_l1b.detector_attrNames:
            logger.info("AC for detector: %s..." % detector_name)
            detector = getattr(enmap_l1b, detector_name)
            detector.data_l2a = np.full(detector.data.shape, np.NaN, dtype=np.float)

            meta = getattr(enmap_l1b.meta, detector_name)
            logger.info("Performing columnwise ac...")
            for icol in tqdm(range(meta.ncols), disable=fo.disable_progressbars):
                for irow in range(meta.nrows):
                    detector.data_l2a[irow, icol, :] = fo.surf_ref(
                        dt=detector.data[irow, icol, :],
                        xx=np.array([cwv[irow, icol], a[irow, icol], b[irow, icol], cwc[irow, icol]]),
                        pt=fo.pt[irow, icol, :], mode=detector_name)
                    if detector_name == "swir":
                        if ice is None:
                            swir_feature = fo.rho_beer_lambert(
                                np.array([cwv[irow, icol], a[irow, icol], b[irow, icol], cwc[irow, icol]]))
                        else:
                            swir_feature = fo.rho_beer_lambert(
                                np.array([cwv[irow, icol], a[irow, icol], b[irow, icol], cwc[irow, icol],
                                          ice[irow, icol]]))
                        detector.data_l2a[irow, icol, fo.fit_wvl] = swir_feature


def sicor_ac_enmap(enmap_l1b, options, logger=None):
    """
    Atmospheric correction for EnMAP Level-1B products, including a three phases of water retrieval.

    :param enmap_l1b: EnMAP Level-1B object
    :param options:   Dictionary with EnMAP specific options
    :param logger:    None or logging instance
    :return:          surface reflectance, water vapor, liquid water and ice maps
    """
    logger = logger or logging.getLogger(__name__)

    logger.info("Setting up forward operator...")
    fo_enmap = Fo(enmap_l1b=enmap_l1b, options=options, logger=logger)

    logger.info("Setting up forward operator function...")
    fo_func_enmap = FoFunc(fo=fo_enmap)

    logger.info("Starting 3 phases of water retrieval...")
    cwv_model, cwc_model, ice_model, a_model, b_model, toa_model, se, scem, srem = __minimize__(
        fo=fo_enmap, opt_func=fo_func_enmap, logger=logger, oe=options["EnMAP"]["Retrieval"]["fast"],
        ice=options["EnMAP"]["Retrieval"]["ice"])

    if fo_enmap.segmentation:
        data_ac = fo_enmap.rdn_subset
    else:
        data_ac = enmap_l1b

    logger.info("Starting surface reflectance retrieval...")
    warnings.filterwarnings("ignore")
    if options["EnMAP"]["Retrieval"]["ice"]:
        make_ac_enmap(data=data_ac, enmap_l1b=enmap_l1b, fo=fo_enmap, cwv=cwv_model, cwc=cwc_model, ice=ice_model,
                      a=a_model, b=b_model, logger=logger)
    else:
        make_ac_enmap(data=data_ac, enmap_l1b=enmap_l1b, fo=fo_enmap, cwv=cwv_model, cwc=cwc_model, ice=None, a=a_model,
                      b=b_model, logger=logger)

    enmap_l2a_vnir = enmap_l1b.vnir.data_l2a
    enmap_l2a_swir = enmap_l1b.swir.data_l2a

    # apply empirical line solution to extrapolate L2A data for each pixel
    if fo_enmap.segmentation:
        logger.info("Applying empirical line solution to extrapolate L2A data pixelwise...")
        data_l2a_seg = np.concatenate((enmap_l2a_vnir, enmap_l2a_swir), axis=2)
        reflectance = empirical_line_solution(X=fo_enmap.X, rdn_subset=fo_enmap.rdn_subset, data_l2a_seg=data_l2a_seg,
                                              rows=fo_enmap.enmap_rad_all.shape[0],
                                              cols=fo_enmap.enmap_rad_all.shape[1],
                                              bands=fo_enmap.enmap_rad_all.shape[2], segs=fo_enmap.segs,
                                              labels=fo_enmap.labels, processes=fo_enmap.cpu)

        data_l2a_el = reflectance.reshape(fo_enmap.enmap_rad_all.shape)

        enmap_l2a_vnir = data_l2a_el[:, :, :88]
        enmap_l2a_swir = data_l2a_el[:, :, 88:]

        logger.info("Extrapolating water vapor, liquid water and ice maps...")
        cwv_seg = np.zeros(fo_enmap.enmap_rad_all.shape[:2])
        cwc_seg = np.zeros(fo_enmap.enmap_rad_all.shape[:2])
        ice_seg = np.zeros(fo_enmap.enmap_rad_all.shape[:2])
        for i in range(fo_enmap.segs):
            cwv_seg[fo_enmap.labels == i] = cwv_model[:, i]
            cwc_seg[fo_enmap.labels == i] = cwc_model[:, i]
            if fo_enmap.ice:
                ice_seg[fo_enmap.labels == i] = ice_model[:, i]

        cwv_model = cwv_seg
        cwc_model = cwc_seg
        ice_model = ice_seg

    # simple validation of L2A data
    if np.isnan(enmap_l2a_vnir).any() or np.isnan(enmap_l2a_swir).any():
        logger.warning("The surface reflectance generated by SICOR contains NaN values. Please check for errors in the"
                       "input data, the options file, or the processing code.")
    for ii, dl2a in zip(range(2), [enmap_l2a_vnir, enmap_l2a_swir]):
        if dl2a[np.isfinite(dl2a)].shape[0] > 0:
            if ii == 0:
                d_name = "VNIR L2A"
            else:
                d_name = "SWIR L2A"
            if np.min(dl2a[np.isfinite(dl2a)]) < 0:
                logger.warning("%s data contain negative values indicating an overcorrection. Please check for "
                               "errors in the input data, the options file, or the processing code." % d_name)
            if np.max(dl2a[np.isfinite(dl2a)]) > 1:
                logger.warning("%s data contain values exceeding 1 indicating a saturation. Please check for "
                               "errors in the input data, the options file, or the processing code." % d_name)

    del enmap_l1b.vnir.data_l2a
    del enmap_l1b.swir.data_l2a

    logger.info("EnMAP atmospheric correction successfully finished!")

    return enmap_l2a_vnir, enmap_l2a_swir, cwv_model, cwc_model, ice_model, toa_model, se, scem, srem
