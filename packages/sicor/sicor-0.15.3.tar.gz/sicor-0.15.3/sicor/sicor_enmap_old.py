#!/usr/bin/env python
# coding: utf-8
"""Sensor Independent  Atmospheric CORrection (SICOR) AC module - EnMAP specific parts."""

import logging
import hashlib
from datetime import datetime
import numpy as np
from os import path
import pickle
import gzip
from sicor.Tools import SolarIrradiance
from tqdm import tqdm
from itertools import product
from typing import Sequence

from enpt.model.images import EnMAPL1Product_SensorGeo

from sicor.AC.RtFo import FF
from sicor.AC.RtFo import __minimize__
from sicor.AC.RtFo import RtFo, sat
from sicor.AC.ACG import get_pt_names_and_indexes
from sicor.ECMWF import ECMWF_variable
from sicor.Tools import inpaint

__all__ = ["tqdm", "get_hash", "sensor_name", "time2step", "enmap_cache_file",
           "convert_at_sensor_radiance_to_reflectance", "dump_tables_to_buffer_file",
           "load_tables_from_buffer_file", "wavelength_grid_for_response_functions",
           "load_fos_enmap", "get_atmospheric_state", "get_aerosol_model_from_ecmwf",
           "get_state_from_ECMWF", "make_ac", "optimize_inverse_table", "sicor_ac_enmap",
           "Rj2RhoJ_LinX1X2", "Rho2Rj_LinX1X2", "determine_pixels_to_be_processed"]


def get_hash(*args):
    """Compute hash for arbitrary arguments which are supported by hashlib.sha1.
    Intended for numpy.ndarrays and encoded strings.
    :param: e.g. "test".encode('utf-8'))
    :returns: hexstring
    """
    return hashlib.sha1("".join([hashlib.sha1(arg).hexdigest() for arg in args]).encode('utf-8')).hexdigest()


def sensor_name(detector: str, icolumn: int) -> str:
    """Generate a unique detector name for EnMAP detector columns

    :param detector: string, e.g. 'VNIR' or 'SWIR'
    :param icolumn: integer, number of column, 0-999
    """
    return "EnMAP_%s_%i" % (detector, icolumn)


def time2step(date: datetime):
    """"From datetime object to step for ECMEF variable, step is hours in UTC time."""
    return date.hour + date.minute / 60 + date.second / 60 ** 2


def enmap_cache_file(data: EnMAPL1Product_SensorGeo, rtfos: list, buffer_dir=None) -> str:
    """Compute hash for EnMAP product, considered are wavelength calibration and smile
    :param rtfos: list for radiative transfer forward operators
    :param data: EnMAP Level-1B object
    :param buffer_dir: None or string to directory where cache files are stored
    :returns: None if buffer dir is none, else path to cache file
    """
    hash_value = get_hash(
        *[getattr(getattr(data.meta, detector), att)
          for detector in ("vnir", "swir")
          for att in ("wvl_center", "fwhm", "smile")])

    return None if buffer_dir is None else path.join(
        buffer_dir, "{rtfos}_{hash}.pkl.zip".format(
            hash=hash_value,
            rtfos="_".join(rtfos)
        )
    )


def convert_at_sensor_radiance_to_reflectance(enmap_l1b, sensors: dict,
                                              sun_earth_distance_AU=1) -> None:
    """Convert at-sensor radiance to reflectance - this happens in-place.
    :param enmap_l1b: EnMAP Level-1B object
    :param sensors: Dictionarx with sensor specification
    :param sun_earth_distance_AU: Sun Earth distance in AU
    """
    for detector_name in enmap_l1b.detector_attrNames:
        detector = getattr(enmap_l1b, detector_name)
        meta = getattr(enmap_l1b.meta, detector_name)
        if meta.unit == 'mW m^-2 sr^-1 nm^-1':
            for icol in np.arange(meta.ncols):
                sol_irr = sensors[sensor_name(detector_name, icol)]['sol_irr']
                detector.data[:, icol, :] *= (np.pi * sun_earth_distance_AU ** 2 /
                                              sol_irr / enmap_l1b.meta.mu_sun)
            detector.unit = "1"

        else:
            raise ValueError("Reflectance unit %s not understod." % meta.unit)


def dump_tables_to_buffer_file(buffer_file: str, sensors: dict, fos: dict) -> None:
    """Dump AC tables for specific sensos (smile) to disk
    :param buffer_file: File path for buffer file
    :param sensors: Dictionary with sensor definitions
    :param fos: Dictionary with names and coresponding forward operators
    :returns None
    """
    if buffer_file is not None:
        with gzip.open(buffer_file, "wb") as fl:
            pickle.dump(sensors, fl)  # dump sensor specifications (response functions with smile)
            pickle.dump(  # dump tables for AC, including smile
                {fo_name: {attr: getattr(fo, attr) for attr in ("L0", "T_UP", "E_DN", "SS")}
                 for fo_name, fo in fos.items()}, fl)


def load_tables_from_buffer_file(buffer_file: str, options: dict, logger=None) -> (dict, dict):
    """Load ac tables from buffer file.
    :param options: Dictionary with options.
    :param buffer_file: File path to buffer file
    :param logger: None or logging instance
    :returns: (sensors: dict, fos: dict)
    """
    logger = logger or logging.getLogger(__name__)
    with gzip.open(buffer_file, "rb") as fl:
        sensors = pickle.load(fl)
        fos_buffer_tables = pickle.load(fl)

    fos = {}
    for rtfo_name, buffer_table in fos_buffer_tables.items():
        logger.info("Restore: %s" % rtfo_name)
        fos[rtfo_name] = RtFo(
            sensors=sensors,
            buffer_tables=buffer_table, **options["RTFO"][rtfo_name])

    return sensors, fos


def table_to_array(k_wi, a, b, col_wvl, col_k):
    """
    Convert imaginary parts of refractive indexe pandas table to numpy array.
    :param k_wi: imaginary part of refractive index
    :param a: start line
    :param b: end line
    :param col_wvl: wavelength column in pandas table
    :param col_k: k column in pandas table
    :return:
    """
    wvl_ = []
    k_ = []
    for ii in range(a, b):
        wvl = k_wi.at[ii, col_wvl]
        k = k_wi.at[ii, col_k]
        wvl_.append(wvl)
        k_.append(k)
    wvl_arr = np.asarray(wvl_)
    k_arr = np.asarray(k_)

    return wvl_arr, k_arr


def wavelength_grid_for_response_functions(wvl_center: np.ndarray, fwhm: np.ndarray,
                                           wvl_rsp_sampling: float) -> np.ndarray:
    """Make wavelength grid for sampling of response functions for given detector
    :param wvl_center: Numpy array for center wavelength for detector
    :param fwhm: Numpy array of full width half maximum values corresponding to wvl_center vector
    :param wvl_rsp_sampling: Spectral sampling width
    :returns: Numpy array with wavelength grid for sampling of response function
    """
    return np.arange(np.min(wvl_center) - 3 * np.max(fwhm), np.max(wvl_center) + 3 * np.max(fwhm), wvl_rsp_sampling)


def load_fos_enmap(enmap_l1b, options: dict, logger=None):
    """For arbitrary smile and response functions, computing the forward operator (fo) and solar irradiance values
    takes time (~30m). Since smile is not assumed to change fast, caching to disk is implemented. A hash over
    relevant field is used to determine whether to load form disk to to recompute and persist to disk.
    :param logger: None or logging instance
    :param options: Dictionary with options
    :param enmap_l1b: EnMAP Level-1B Product
    :param options: Dictionary with options
    :returns (sensors:dict, fos:dict)

    Side effect: attempts to write / read results to a buffer file, controlled in: options["EnMAP"]["buffer_dir"]
    """
    logger = logger or logging.getLogger(__name__)
    buffer_file = enmap_cache_file(
        data=enmap_l1b, buffer_dir=options["EnMAP"]["buffer_dir"], rtfos=options['EnMAP']['use_only_rtfo'])
    if buffer_file is not None and path.isfile(buffer_file):
        try:
            logger.info("Try to read from: %s" % buffer_file)
            sensors, fos = load_tables_from_buffer_file(buffer_file, options, logger)
        except Exception:
            logger.exception(
                "Error encountered when reading buffer file: %s. Delete file and try again." % buffer_file)
            raise

    else:  # compute tables for given smile, fwhm, and central wavelengths
        logger.info("No buffer file found, compute tables (this may take a while):%s" % buffer_file)
        logger.info("This happens always for changes in the calibration of: central wavelength,")
        logger.info("full width half maximum, and smile coefficients.")
        # get solar irradiance model
        solar = SolarIrradiance(dataset=options["EnMAP"]['solar_model'])
        # get wavelength grid for response functions for each detector
        sensors = {}
        s2f = 2.0 * np.sqrt(2.0 * np.log(2.0))  # convert fwhm to sigma (gaussian parametrisation)
        for detector_name in enmap_l1b.detector_attrNames:
            meta = getattr(enmap_l1b.meta, detector_name)
            logger.info("Prepare spectral response functions for:%s" % detector_name)
            wvl_rsp = wavelength_grid_for_response_functions(
                meta.wvl_center, meta.fwhm, options["EnMAP"]["wvl_rsp_sampling"])

            for icol in tqdm(np.arange(meta.ncols), disable=options["RTFO"]["aerosol_0"]["disable_progress_bars"]):
                sensors[sensor_name(detector_name, icol)] = sat(
                    rspf_type="gaussian",
                    wvl_inst=meta.wvl_center + meta.smile[icol, :],
                    solar=solar, sigma=meta.fwhm / s2f,
                    wvl_rsp=wvl_rsp)

        logger.info("Prepare AC tables: %s " % ",".join(sorted(options["RTFO"].keys())))
        fos = {}
        for rtfo_name, opts in sorted(options["RTFO"].items()):

            if rtfo_name in options["EnMAP"]["use_only_rtfo"]:
                logger.info("Prepare for table: %s" % rtfo_name)
                fos[rtfo_name] = RtFo(sensors=sensors, **opts)
            else:
                logger.info("Skip table '%s' from LUT since it is not given in 'EnMAP/use_only_rtfo'=%s options. " % (
                    rtfo_name, str(options["EnMAP"]["use_only_rtfo"])))

        # dump results to disk
        dump_tables_to_buffer_file(str(buffer_file), sensors, fos)

    return sensors, fos


def get_atmospheric_state(fos: dict, enmap_l1b, options: dict, logger=None) -> dict:
    """Set up atmospheric state variables for both detectors.
    :param fos: Dictionary with forward operators
    :param enmap_l1b: EnMAP Level-1B product
    :param options: dictionary with options
    :param logger: None or logging instance


    assuming that detector names are "vnir" and "swir"
    :returns state: {"p0": {"vnir": np.ndarray, "swir": np.ndarray},  # background state
                     "e0": {"vnir": np.ndarray, "swir": np.ndarray},  # error if state
                     "ac": {"vnir": np.ndarray, "swir": np.ndarray},  # ac map, where to perform ac
                     }

    Side effect: Adds "settings" dictionary to options dictionary
    """

    logger = logger or logging.getLogger(__name__)

    settings = {
        "fo_instances": {k: {"flag": v["flag"]} for k, v in options["RTFO"].items() if k in fos},
        "atm_fields": list({i for v in options["RTFO"].values() for k in ("dim_atm", "dim_scat") for i in v[k]})
    }
    pt_names, pt_indexes, flag_to_indexes_res, flag_to_indexes_common, fo_flags = get_pt_names_and_indexes(fos,
                                                                                                           settings)

    options["settings"] = settings
    options["settings"]["pt_names"] = list(pt_names)
    options["settings"]["pt_indexes"] = pt_indexes
    logger.info(options["settings"])

    # see docstring of method for more info
    state = {i: {detector_name: np.zeros(
        # dim: 2D of image + number of atm state parameters
        list(getattr(enmap_l1b, detector_name).data.shape[:2]) + [len(options["settings"]["pt_names"])],
        dtype=np.float) for detector_name in enmap_l1b.detector_attrNames}
             for i in ["p0", "e0"]}
    state["ac"] = {detector_name: np.full(
        shape=state["p0"][detector_name].shape[:2],
        fill_value=False, dtype=np.bool) for detector_name in enmap_l1b.detector_attrNames}

    state["le0"] = {}
    for detector_name in enmap_l1b.detector_attrNames:
        detector = getattr(enmap_l1b, detector_name)
        meta = getattr(enmap_l1b.meta, detector_name)
        if meta.snr is not None:
            state["le0"][detector_name] = detector.data[:] / meta.snr[:]
        else:
            state["le0"][detector_name] = None
            logger.warning("No SNR present in EnMAP product -> continue without.")

    def test_for(current_name, name):
        """

        :param current_name:
        :param name:
        :return:
        """
        return current_name == name and current_name not in options["EnMAP"]["keep_defaults_for"]

    # set default values as given in options["EnMAP"]['default_values']
    for default_name, default_value in options["EnMAP"]['default_values'].items():
        for detector_name in enmap_l1b.detector_attrNames:
            st = state["p0"][detector_name][:, :, options["settings"]["pt_names"].index(default_name)]

            if test_for(default_name, "sza"):
                st[:, :] = enmap_l1b.meta.geom_sun_zenith
            elif test_for(default_name, "vza"):
                st[:, :] = enmap_l1b.meta.geom_view_zenith
            elif test_for(default_name, "azi"):
                st[:, :] = enmap_l1b.meta.geom_sun_azimuth - enmap_l1b.meta.geom_view_azimuth
            else:
                st[:, :] = default_value

            logger.info("Set defaults for %s: %s = %.2f" % (
                detector_name, default_name, float(np.mean(st[:, :]))))

    return state


def get_state_from_ECMWF(state: dict, enmap_l1b, options: dict, logger=None):
    """Get AOT fiel from ECMWF forecast and override in state parameter.
    :param state: State dictionary, as instantiated by 'get_atmospheric_state' function
    :param enmap_l1b: EnMAP Level-1B product
    :param options: Options dictionary
    :param logger: None of logging instance
    :returns: None
    """

    for detector_name in enmap_l1b.detector_attrNames:
        meta = getattr(enmap_l1b.meta, detector_name)
        logger.info("Get ECMWF data for detector: %s" % detector_name)
        for var_sicor, var_ecmwf in options["ECMWF"]["mapping"].items():
            if var_sicor not in options["EnMAP"]["keep_defaults_for"]:
                st = state["p0"][detector_name][:, :, options["settings"]["pt_names"].index(var_sicor)]
                try:
                    st[:, :] = options["ECMWF"]["conversion"][var_sicor] * ECMWF_variable(
                        variable=var_ecmwf,
                        path_db=options["ECMWF"]["path_db"],
                        var_date=enmap_l1b.meta.observation_datetime)(
                            step=time2step(enmap_l1b.meta.observation_datetime),
                            lons=meta.lons,
                            lats=meta.lats,
                            shape=(meta.nrows, meta.ncols))
                    logger.info("mean(%s) = mean(%s) = %.2f" % (
                        var_sicor, var_ecmwf, float(np.mean(st[:, :]))))
                except Exception:
                    logger.info("ECMWF for {var} not present.".format(var=var_ecmwf))


def get_aerosol_model_from_ecmwf(enmap_l1b, options: dict, logger=None) -> None:
    """Determine aerosol model from ECMWF aerosol type fraction.
    Conversion is defined in options["ECMWF"]['var2type'].
    :param enmap_l1b: EnMAP Level-1B product
    :param options: Options dictionary
    :param logger: None or logging instance
    :returns None

    Changes: options["EnMAP"]["aerosol_model"]

    """
    logger = logger or logging.getLogger(__name__)
    try:
        aerosol_model_fraction = {k: 0 for k in options["ECMWF"]['var2type'].values()}
        for detector_name in enmap_l1b.detector_attrNames:
            meta = getattr(enmap_l1b.meta, detector_name)

            bf_a = np.mean(ECMWF_variable(
                variable=options["ECMWF"]['mapping']["tau_a"],
                path_db=options["ECMWF"]["path_db"],
                var_date=enmap_l1b.meta.observation_datetime)(
                    step=time2step(enmap_l1b.meta.observation_datetime),
                    lons=meta.lons,
                    lats=meta.lats,
                    shape=(meta.nrows, meta.ncols)))
            logger.info("Mean AOT for detector %s = %.2f " % (detector_name, bf_a))

            for ecmwf_type, table_type in options["ECMWF"]['var2type'].items():
                aerosol_model_fraction[table_type] += np.mean(
                    ECMWF_variable(
                        variable=ecmwf_type,
                        path_db=options["ECMWF"]["path_db"],
                        var_date=enmap_l1b.meta.observation_datetime)(
                            step=time2step(enmap_l1b.meta.observation_datetime),
                            lons=meta.lons,
                            lats=meta.lats,
                            shape=(meta.nrows, meta.ncols))) / bf_a

        aerosol_model_fraction = {k: v / sum(aerosol_model_fraction.values())
                                  for k, v in aerosol_model_fraction.items()}
        for model, value in aerosol_model_fraction.items():
            logging.info("aot fraction(%s) = %.2f " % (model, value))
        options["EnMAP"]["aerosol_model"] = max(aerosol_model_fraction, key=aerosol_model_fraction.get)
    except FileNotFoundError:
        logger.exception("ECMWF data for aerosol not found, continue with default value: %s " % options[
            "EnMAP"]["aerosol_default"])
        options["EnMAP"]["aerosol_model"] = options["EnMAP"]["aerosol_default"]

    logger.info("Chosen aerosol model from ECMWF: %s" % options["EnMAP"]["aerosol_model"])


def make_ac(enmap_l1b, state: dict, options: dict, fos: dict, logger=None) -> None:
    """Perform ac for enmap_l1b, based on parameters given in state.
    :param state: State dictionary, as instantiated by 'get_atmospheric_state' function
    :param enmap_l1b: EnMAP Level-1B product
    :param options: Options dictionary
    :param fos: dictionary of forward operators
    :param logger: None or logging instance
    :return: None

    Side effect: adds 'data_l2a' attribute to each detector. This numpy array holds
    the surface reflectance map.
    """
    logger = logger or logging.getLogger(__name__)
    fo = fos[options["EnMAP"]['aerosol_model']]
    fo.set_luts("orig")
    for detector_name in enmap_l1b.detector_attrNames:
        logger.info("AC for detector: %s" % detector_name)
        detector = getattr(enmap_l1b, detector_name)
        detector.data_l2a = np.full(detector.data.shape, np.NaN, dtype=np.float)

        meta = getattr(enmap_l1b.meta, detector_name)
        logger.info("Perform columnwise ac")
        for icol in tqdm(range(meta.ncols), disable=options["RTFO"]["aerosol_0"]["disable_progress_bars"]):
            fo.set_sensor(sensor_name(detector_name, icol))
            fo.interpolation_settings(jacobean=False, caching=False)
            for irow in range(meta.nrows):
                if state["ac"][detector_name][irow, icol] is np.True_:
                    detector.data_l2a[irow, icol, :] = fo.reflectance_boa(
                        pt=state["p0"][detector_name][irow, icol, :],
                        toa_reflectance=detector.data[irow, icol, :])

                    if detector_name == "swir":
                        detector.data_l2a[irow, icol, 40:49] = np.nan
                        detector.data_l2a[irow, icol, 81:97] = np.nan


class Rj2RhoJ_LinX1X2(object):
    """Linear Surface reflectance model.
     Derived using sympy:

        from sympy import Symbol, Function, Eq, solveset, linsolve, simplify, diff
        a, b, x1, x2, y1, y2, x, y = symbols("a b x1 x2 y1 y2 x, y")
        f = a*x + b
        aa,bb =  list(linsolve([f.subs(x,x1) - y1,f.subs(x,x2) -y2], [a,b]))[0]
        ff = simplify(f.subs(a,aa).subs(b,bb))

        print("f =",f)
        print("f =",ff)
        print("df/y1 =",diff(ff,y1))
        print("df/y2 =",diff(ff,y2))
    """

    def __init__(self, x1: float, x2: float, x: np.ndarray):
        """Linear surface reflectance model.
        Two model parameters rj[0] and rj[1] give the surface reflectance value
        at wavelength x1 and x2.
        :type x: Wavelength array
        :type x2: 2nd wavelentgh parameter
        :type x1: 1st wavelentgh parameter
        """
        self.x1 = x1
        self.x2 = x2
        self.x = x
        self.wvl = self.x
        self.n_rho_lin = 2
        self.j = np.array([
            (x - x2) / (x1 - x2),
            (x1 - x) / (x1 - x2)
        ])

    def __call__(self, rj):
        """Linear reflectance model with values rj[0] at x1 and rj[1] at x2 for wavelengths x."""
        y1, y2 = rj
        return (
            (self.x * (y1 - y2) + self.x1 * y2 - self.x2 * y1) / (self.x1 - self.x2),  # Rho
            self.j)  # Jacobean


class Rho2Rj_LinX1X2(object):
    """Inverse model class for Rj2RhoJ_LinX1X2."""

    def __init__(self, x1: float, x2: float, x: np.ndarray):
        """Inverse init for Rj2RhoJ_LinX1X2."""
        self.x1 = x1
        self.x2 = x2
        self.x = x
        self.wvl = self.x
        self.n_rho_lin = 2

    def __call__(self, rho):
        return np.interp(x=[self.x1, self.x2], xp=self.x, fp=rho)


def optimize_inverse_table(enmap_l1b: EnMAPL1Product_SensorGeo, fo, options: dict, sensors: dict, state: dict,
                           detector_name: str, logger=None, wvl_center=762.5, wvl_bands_intervall=[1, 2], dim_opt="spr",
                           dim_red=("azi", "coz", "vza", "tau_a", "cwv", "tmp"), inverse_tables_sampling=(3, 3, 3),
                           n_pca=None) -> np.ndarray:
    """
    Optimize free parameter by means of interpolation in inverse table on unstructured grid. Assumed is a simple
    two parametric surface reflectance model.

    :param inverse_tables_sampling: three tuple of integer, gives inverse table sampling for
        rho1, rho2, and the free parameter
    :param enmap_l1b: EnMAP Level-1B product
    :param fo: forward operators object
    :param options: Options dictionary
    :param sensors: Sensor definition dictionary.
    :param state: State dictionary.
    :param logger: None or logging instance
    :param detector_name: e.g. 'vnir' or 'swir'
    :param wvl_center: Wavelength to select bands around based on [wvl_bands_interval]
    :param wvl_bands_intervall: Two list / tuple / ... Two ints, number of bands to the
        'left' and 'right' part of the spectrum centreed at [wvl_center]
    :param dim_opt: String, name of to be optimized parameter
    :param dim_red: list of parameter for which luts are reduced
    :param n_pca: None or Number of principle components considered for dimensionality reduction,
        is None is given, no PCA is performed
    :return: Numpy array with results for detector and dim_red
    """
    from scipy.interpolate import griddata  # import here to avoid static TLS ImportError

    logger = logger or logging.getLogger(__name__)
    detector = getattr(enmap_l1b, detector_name)
    meta = getattr(enmap_l1b.meta, detector_name)

    res = np.zeros(detector.data.shape[:2])
    res[:] = np.NaN

    reduce_vars = {var: np.mean(state["p0"][detector_name][:, :, options["settings"]['pt_names'].index(var)])
                   for var in dim_red}

    for k, v in reduce_vars.items():
        logger.info("Reduce %s -> %s" % (k, v))

    fo.set_luts("orig")
    fo.reduce_luts("reduced_luts", reduce_vars)
    fo.set_luts("reduced_luts")

    for icol in tqdm(range(0, meta.ncols), disable=options["RTFO"]["aerosol_0"]["disable_progress_bars"]):
        col_sel = state["ac"][detector_name][:, icol]
        if np.sum(col_sel) > 0:
            sn = sensor_name(detector_name, icol)
            wv = sensors[sn]['wvl_inst']
            fo.set_sensor(sn)
            fo.interpolation_settings(jacobean=False, caching=False)
            _wvl_sel = (lambda x: np.arange(
                x - wvl_bands_intervall[0],
                x + wvl_bands_intervall[1]))(np.argmin(np.abs(wv - wvl_center)))  # list of integer numbers
            wvl_sel = np.zeros(wv.shape, dtype=np.bool)  # bool array with length of wavelengths
            wvl_sel[_wvl_sel] = True

            # surface reflectance model with Jacobean.
            # considered is one characteristic absorption feature of the parameter to be optimized.
            # from the first two enmap channel positions of the absorption feature the linear reflectance model
            # is build for the whole wavelength range (either vnir or swir)

            # linear surface reflectance model: f = a*x + b (linear continuum).
            # since a and b are unknown, the model is converted to a function of wavelengths from both continuum levels
            # (x1,x2) and their associated surface reflectance values (y1,y2); x represents all wavelengths:
            # f = (x * (y1 - y2) + x1 * y2 - x2 * y1) / (x1 - x2)
            Rj2RhoJ = Rj2RhoJ_LinX1X2(x1=wv[wvl_sel][0], x2=wv[wvl_sel][1], x=wv)

            pt = np.zeros(np.max(fo.L0["idx"] + 1), dtype=np.float)
            ids = {dim: fo.L0["idx"][fo.L0["dims"].index(dim)] for dim in [dim_opt]}

            mm_arr = np.mean(detector.data[:, icol, :], axis=0)
            mm_std = np.std(detector.data[:, icol, :])

            pt[ids[dim_opt]] = np.median(fo.dims[dim_opt])

            # estimate surface reflectance by interpolating within the LUT for an atmospheric state containing
            # only the median value from the LUT of the parameter to be optimized.
            # a1,a2: for each wavelength the mean from all pixels per column minus three times the standard deviation
            # is chosen as basic TOA reflectance.
            # b1,b2: for each wavelength the mean from all pixels per column plus three times the standard deviation is
            # chosen as basic TOA reflectance.
            # the surface reflectance is estimated for the two continuum levels of the chosen absorption feature
            a1, a2 = fo.reflectance_boa(pt, toa_reflectance=mm_arr - 3 * mm_std)[wvl_sel][[0, -1]]
            b1, b2 = fo.reflectance_boa(pt, toa_reflectance=mm_arr + 3 * mm_std)[wvl_sel][[0, -1]]

            values = []
            points = []

            # build parameter grid for interpolation on unstructured grid
            n_rho1, n_rho2, n_xx = inverse_tables_sampling

            # build a 3-dimensional grid containing the surface reflectance of the two continuum levels of the
            # absorption feature and the concentration of the parameter to be optimized,
            # each dimension has 3 grid points

            # build the cartesian product of all input values,
            # e.g., product((0,1), (0,1), (0,1)) --> (0,0,0) (0,0,1) (0,1,0) (0,1,1) (1,0,0)
            params = product(*(
                [np.linspace(a1, b1, n_rho1)] +
                [np.linspace(a2, b2, n_rho2)] +
                [np.linspace(np.min(fo.dims[dim]), np.max(fo.dims[dim]), n_xx) for dim in [dim_opt]]
            ))

            # loop through all combinations of the cartesian product and estimate for each the surface reflectance
            # spectrum based on the before initialized linear model using the two reflectance values of the continuum
            # levels.
            # based on the estimated surface reflectance spectrum and the associated parameter value,
            # the TOA reflectance values for the chosen absorption feature are modeled for each combination of the
            # cartesian product
            for ii, (rho1, rho2, xx) in enumerate(params):
                pt[ids[dim_opt]] = xx
                rho = Rj2RhoJ([rho1, rho2])[0]
                rfl = fo.reflectance_toa(pt, rho)[wvl_sel]

                points.append(rfl)
                values.append(xx)
            # table for interpolation on unstructured grid
            points = np.stack(points)  # reflectance spectra for sampled variation of rho1, rho2, and xx
            values = np.stack(values)  # corresponding values for dim_opt

            if n_pca is not None:
                from sklearn.decomposition import PCA  # import here to avoid static TLS ImportError

                pc = PCA(n_components=n_pca).fit(detector.data[col_sel, icol, :][:, wvl_sel])
                rr = griddata(
                    pc.transform(points),
                    values[:],
                    pc.transform(detector.data[col_sel, icol, :][:, wvl_sel]))
            else:
                # for each absorption feature spectrum of the enmap data, the parameter value is interpolated from
                # the unstructured grid of points and values
                rr = griddata(
                    points, values,
                    detector.data[col_sel, icol, :][:, wvl_sel])

            res[col_sel, icol] = rr

    return res


def determine_pixels_to_be_processed(state: dict, enmap_l1b: EnMAPL1Product_SensorGeo, options: dict, logger=None):
    """Determines the pixels that should be processes (all True marked ones in state["ac"][detector_name]).
    :param state: State dictionary
    :param enmap_l1b: EnMAP Level-1B product.
    :param options: Options dictionary
    :param logger: logging instance or None
    :return: None -> state["ac"] is altered
    """
    logger = logger or logging.getLogger(__name__)
    for flag in options["EnMAP"]['scene_detection_flags_to_process']:
        for detector_name in enmap_l1b.detector_attrNames:
            logger.info("Included flag: %.1f for: %s" % (flag, detector_name))
            state["ac"][detector_name][getattr(enmap_l1b, detector_name).mask_clouds[:] == flag] = True

    logger.info("#### insert dummy ac map, remove in future ####")
    logger.info("#### insert dummy ac map, remove in future ####")
    logger.info("#### insert dummy ac map, remove in future ####")
    state["ac"]["swir"][:] = True
    state["ac"]["swir"][25:45, 456:678] = False
    state["ac"]["vnir"][:] = True
    state["ac"]["vnir"][25:45, 256:378] = False


def sicor_ac_enmap(enmap_l1b: EnMAPL1Product_SensorGeo, options: dict, logger=None, debug=False)\
        -> EnMAPL1Product_SensorGeo:
    """Atmospheric correction for EnMAP Level-1B products.
    :param debug: debug mode: True / False
    :param enmap_l1b: EnMAP Level-1B object
    :param options: Dictionary with options
    :param logger: None or logging instance.
    :returns enmap_level_2a0, state: (Surface reflectance in sensor geometry product, dict with ac state)
    """
    logger = logger or logging.getLogger(__name__)
    # load ac tables and forward operator
    sensors, fos = load_fos_enmap(enmap_l1b, options, logger)
    # convert at-sensor radiance to reflectance
    logger.info("Convert radiance to reflectance")
    convert_at_sensor_radiance_to_reflectance(enmap_l1b, sensors)

    # get state variable, fill with default values
    state = get_atmospheric_state(fos, enmap_l1b, options, logger=logger)
    determine_pixels_to_be_processed(state, enmap_l1b, options, logger)

    # get parameters from ECMWF (if desired)
    get_state_from_ECMWF(state, enmap_l1b, options, logger)
    # select aerosol type
    if options["EnMAP"]["aerosol_model"] == "ECMWF":
        logger.info("Determine aerosol type from ECMWF")
        get_aerosol_model_from_ecmwf(enmap_l1b, options, logger)
    else:
        logger.info("Use given aerosol type: %s" % options["EnMAP"]["aerosol_model"])

    logger.info("####### Remove #############")
    options["EnMAP"]["aerosol_model"] = "aerosol_0"
    logger.info("####################")

    # check is model is available
    if options["EnMAP"]["aerosol_model"] not in fos.keys():
        raise ValueError("Default aerosol '%s' model not found in forward operator list, available are: %s" % (
            options["EnMAP"]["aerosol_model"], str(list(fos.keys()))))

    # first guess for atmospheric parameters
    # fast retreival trough lookup in inverse table on unstructured grid
    for opts in [
        {
            "detector_name": "vnir", "wvl_center": 762.5, "wvl_bands_intervall": [1, 2],
            "fo":fos[options["EnMAP"]['aerosol_model']],
            "dim_opt": "spr", "dim_red": ("azi", "coz", "vza", "tau_a", "cwv", "tmp"), "n_pca": None
        },
        {
            "detector_name": "vnir", "wvl_center": 900.0, "wvl_bands_intervall": [2, 2],
            "fo": fos[options["EnMAP"]['aerosol_model']],
            "dim_opt": "cwv", "dim_red": ("azi", "coz", "vza", "tau_a", "spr", "tmp"), "n_pca": None
        },
        {
            "detector_name": "swir", "wvl_center": 960.0, "wvl_bands_intervall": [2, 2],
            "fo": fos[options["EnMAP"]['aerosol_model']],
            "dim_opt": "cwv", "dim_red": ("azi", "coz", "vza", "tau_a", "spr", "tmp"), "n_pca": None
        },
        {
            "detector_name": "swir", "wvl_center": 2380.0, "wvl_bands_intervall": [2, 2],
            "fo": fos["ch4"],
            "dim_opt": "ch4", "dim_red": ("azi", "coz", "vza", "tau_a", "spr", "cwv", "tmp"), "n_pca": None
        }
    ]:
        if opts["dim_opt"] not in options["EnMAP"]["keep_defaults_for"]:
            logger.info("Estimate %s from data." % opts["dim_opt"])
            res = optimize_inverse_table(enmap_l1b=enmap_l1b, options=options,
                                         sensors=sensors, state=state, logger=logger, **opts)

            if np.sum(np.isfinite(res)) > 0.7 * np.sum(state["ac"][opts["detector_name"]]):
                logger.info("Put fg to state for: %s" % opts["dim_opt"])
                inpaint(res, sigma=1.0, logger=logger, fill_remaining="broom", update_in_place=True)
                state['p0'][opts["detector_name"]][:, :, options["settings"]['pt_names'].index(
                    opts["dim_opt"])] = res

    # full spectral fit, per column, per pixel
    fit_options = {
        "cwv": {
            "sensors": sensors, "state": state,
            "enmap_l1b": enmap_l1b, "detector_name": "vnir", "options": options, "fo": fos["aerosol_0"],
            "optimize_dims_atm": ("cwv",), "wvl_center": 950.0, "wvl_bands_intervall": (8, 5),
            "reduced_luts": {"azi": 0.0, "coz": 350.0, "vza": 0.0, "tau_a": 0.2, "tmp": 0},
            "pt_index": options["settings"]['pt_indexes']['aerosol_0'], "debug": debug},

        "ch4": {
            "sensors": sensors, "state": state,
            "enmap_l1b": enmap_l1b, "detector_name": "swir", "options": options, "fo": fos["ch4"],
            "optimize_dims_atm": ("ch4",), "wvl_center": 2380.0, "wvl_bands_intervall": (15, 7),
            "reduced_luts": {"azi": 0.0, "coz": 350.0, "vza": 0.0, "tau_a": 0.2, "cwv": 20.0, "tmp": 0},
            "pt_index": options["settings"]['pt_indexes']['ch4'], "debug": debug
        }
    }
    fits = {fit: optimize(**opts) for fit, opts in fit_options.items()}

    # perform ac
    state["p0"]["vnir"][:, :, 2] = fits["cwv"]["results"][:, :, 0]
    state["p0"]["vnir"][:, :, 8] = fits["ch4"]["results"][:, :, 0]
    state["p0"]["swir"][:, :, 2] = fits["cwv"]["results"][:, :, 0]
    state["p0"]["swir"][:, :, 8] = fits["ch4"]["results"][:, :, 0]

    make_ac(enmap_l1b, state, options, fos, logger)

    return enmap_l1b, state, fits


def optimize(sensors, state, enmap_l1b, detector_name, options, fo, pt_index, optimize_dims_atm: Sequence[str],
             wvl_center: float, wvl_bands_intervall: Sequence[int], reduced_luts: dict, debug=False) -> dict:
    """
    Per column, per pixel spectral fitting for EnMAP Level-1B images. Smile is taken into consideration.

    :param reduced_luts: dict with names of atm. variables and their value to reduce the luts',
        e.g.: {"azi":0.0,"coz":350.0,"vza":0.0,"tau_a":0.2,"cwv":20.0,"tmp":0}
    :param wvl_bands_intervall: 2-tuple, numbers of selected channles blue and red of [wvl_center], e.g. (2,2)
    :param wvl_center: Center wavelength for partial spectral fitting, e.g. 760nm
    :param optimize_dims_atm: tuple with atm names which should be part of the optimization, e.g. ("spr",)

    Currently this is quite slow (but: there are many to-be-fitted spectra within an EnMAP image,
    also: this is generic, for a special case one can implement something faster)
    """

    # get detector and meta data
    detector = getattr(enmap_l1b, detector_name)
    meta = getattr(enmap_l1b.meta, detector_name)
    fo.set_luts("orig")
    fo.reduce_luts("reduced_luts", reduced_luts)
    fo.set_luts("reduced_luts")

    # selection of wavelengths for the spectral fit
    icol_wvn_sel = 0
    sn = sensor_name(detector_name, icol_wvn_sel)
    wv = sensors[sn]['wvl_inst']
    wvl_sel = (lambda x: np.arange(
        x - wvl_bands_intervall[0],
        x + wvl_bands_intervall[1]))(np.argmin(np.abs(wv - wvl_center)))

    # result are stored here:
    fit = {
        "spectra": np.zeros(detector.data[:, :, wvl_sel].shape, dtype=np.float),
        "residuals": np.zeros(detector.data.shape[:2], dtype=np.float),
        "results": np.zeros(list(detector.data.shape[:2]) + [len(optimize_dims_atm) + 2], dtype=np.float)
    }
    for val in fit.values():
        val[:] = np.NaN

    for icol in tqdm(range(meta.ncols), disable=options["RTFO"]["aerosol_0"]["disable_progress_bars"]):
        # select sensor name per column -> smile consideration
        sn = sensor_name(detector_name, icol)
        wv = sensors[sn]['wvl_inst']  # wavelength for this column
        fo.set_sensor(sn)  # actually 'use' this sensor for this fo (forward operator)

        # set a surface reflectance model which computes rho (surface reflectance) for given parameters Rj
        # Rho2Rj: used to compute a first guess
        # Rj2RhoJ: actual surface reflectance model, also computes the Jacobean with respect to Rj's.
        # Feel free to change this. Currently, a simple linear model is used

        # the surface reflectance model and its inverse model are defined and initialized
        # based on the two continuum levels of the absorption feature (wv = all wavelengths)
        fo.set_rho_lin(
            Rho2Rj=Rho2Rj_LinX1X2(x1=wv[wvl_sel][0], x2=wv[wvl_sel][-1], x=wv),
            Rj2RhoJ=Rj2RhoJ_LinX1X2(x1=wv[wvl_sel][0], x2=wv[wvl_sel][-1], x=wv)
        )
        # compute the jacobean of the fo, don't cache results
        fo.interpolation_settings(jacobean=True, caching=False)

        # objective function to be minimized later
        ff = FF(
            fo=fo,  # which forward operator shall be used?
            optimize_dims_atm=optimize_dims_atm,  # which atm parameters are varied for optimization?
            wvl_sel=wvl_sel  # which wavelength channels shall be selected (should be consistent with data)
        )

        p0 = np.copy(state["p0"][detector_name][:, [icol], :])
        # run optimization for each column
        # parameters are: pt_index = [0 1 2 3 4 5 6 7];
        # pt_names = ['spr', 'coz', 'cwv', 'tmp', 'tau_a', 'vza', 'sza', 'azi', 'ch4'];
        # p0 => number of lines and columns equivalent to the enmap scene and 9 state parameters (pressure=1020;
        # ozone=400; water vapor=20; temperature=0; aerosol optical thickness=0.2; viewing zenith angle=7.8;
        # sun zenith angle=34.6; azimuth angle=75.1; methane=3.0).
        # based on the first guess of atmospheric state p0 the function ff is optimized to fit the enmap data
        rr, mm, nr = __minimize__(
            pt_index=pt_index,
            p0=p0,
            pt_names=options["settings"]["pt_names"],
            data=detector.data[:, [icol], :],
            opt_func=ff,
            opt_range="full",
            processes=6,  # simple multiprocessing
            monitor=False,
            debug=False,
            update_p0=True,
            opt_options={
                #  "maxiter": 10,  # more is better, but slower
                "disp": False
            })

        fit["results"][:, icol, :] = rr[:, 0]
        fit["residuals"][:, icol] = nr[:, 0]
        fit["spectra"][:, icol, :] = mm[:, 0, wvl_sel]
        fit["wvl_sel"] = wvl_sel

        if debug is True and icol > 10:
            break

    return fit
