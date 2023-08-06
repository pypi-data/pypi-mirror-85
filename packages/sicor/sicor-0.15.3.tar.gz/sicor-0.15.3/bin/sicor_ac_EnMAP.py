#!/usr/bin/env python
"""Command line program to run sicor for EnMAP Level-1B products."""
import argparse
import logging
from datetime import datetime
from enpt.io.reader import L1B_Reader
import pprint

from sicor.options import get_options
from sicor.sicor_enmap_old import *


def sicor_ac_enmap_parser():
    """Return argument parser for sicor EnMAP"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", action="store", required=True, type=str,
                        help="Path to EnMAP Level-1B product (root dir).")
    parser.add_argument("-s", "--settings", action="store", required=True, type=str,
                        help="Path to settings json file. ")
    parser.add_argument("-o", "--output", action="store", required=True, type=str,
                        help="Path to output directory (will be created if nonexistent).")
    parser.add_argument("--snr_vnir", action="store", required=False, default=None)
    parser.add_argument("--snr_swir", action="store", required=False, default=None)
    parser.add_argument("-q", "--quiet", action="store_true", required=False, default=False)
    parser.add_argument("-d", "--debug", action="store_true", required=False, default=False)

    return parser


if __name__ == "__main__":
    args = sicor_ac_enmap_parser().parse_args()
    logger = logging.getLogger("SICOR_EnMAP")
    logger.setLevel(logging.DEBUG)
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)-10s %(levelname)-10s %(module)-10s - %(funcName)-10s: %(message)s',
        datefmt="%H:%M:%S"
    )

    logger.info("Sicor AC for EnMAP started.")
    logger.info("Input = %s" % args.input)
    logger.info("Output = %s" % args.output)
    logger.info("SNR VNIR = %s" % str(args.snr_vnir))
    logger.info("SNR SWIR = %s" % str(args.snr_swir))
    logger.info("Settings = %s" % args.settings)

    if args.quiet is True:
        logger.info("Disable progressbar due to --quiet parameter.")

        def tqdm_quiet(*args):
            """Quiet version of tqdm status bar."""
            return args[0]
        tqdm = tqdm_quiet

        import sicor.sicor_enmap_old as bf
        bf.tqdm = tqdm_quiet

        import sicor.AC.RtFo as bf
        bf.tqdm = tqdm_quiet

    options = get_options(args.settings)
    logger.info("Load settings: \n" + pprint.pformat(options))

    # Load EnMAP Level-1B Product from file system
    logger.warning("Observation time missing in metadata")  # TODO: Remove this
    enmap_l2a_sens_geo, state, fits = sicor_ac_enmap(
        enmap_l1b=L1B_Reader(logger=logger).read_inputdata(
            root_dir=args.input,
            observation_time=datetime(2015, 12, 7, 10),
            lon_lat_smpl=options["EnMAP"]['lon_lat_smpl'],
            snr_vnir=args.snr_vnir,
            snr_swir=args.snr_swir),
        options=options, logger=logger, debug=args.debug)

    out_fn = enmap_l2a_sens_geo.save(
        outdir=args.output,
        suffix="_surface_reflectance")

    logger.info("Wrote product to: %s" % out_fn)
    logger.info("EEooFF")
