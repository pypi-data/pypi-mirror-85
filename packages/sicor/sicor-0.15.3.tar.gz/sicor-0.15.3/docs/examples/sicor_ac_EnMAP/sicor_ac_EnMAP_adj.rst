
Sicor EnMAP
===========

Noteboook for development and debugging of sicor for EnMAP.

.. code:: python

    #### use in jupyter notebook for debugging ###
    import ipython_memory_usage.ipython_memory_usage as imu
    imu.start_watching_memory()
    %load_ext autoreload
    %autoreload 2


.. parsed-literal::

    In [1] used 0.2148 MiB RAM in 0.11s, peaked 0.00 MiB above current, total RAM usage 41.08 MiB


.. code:: python

    import argparse
    import logging
    from datetime import datetime
    from enpt.io.reader import L1B_Reader
    import pprint
    
    #### use in jupyter notebook for debugging ###
    import matplotlib.pyplot as plt
    %matplotlib inline
    import sys
    from types import SimpleNamespace
    from pathlib import Path
    import os
    from typing import Sequence
    
    from glob import glob
    from os import path
    from zipfile import ZipFile
    sicor_dir = Path(os.getcwd()).parent.absolute()
    sys.path.insert(0,str(sicor_dir))  # make sure sicor is load from local directory
    import sicor; print(sicor)
    ####
    
    from sicor.options import get_options
    from sicor.sicor_enmap import *
    from sicor.AC.RtFo import FF
    from sicor.AC.RtFo import __minimize__
    from sicor.sicor_enmap import optimize


.. parsed-literal::

    <module 'sicor' from '/misc/fluo6/andre/projekte/Sentinel2/py/sicor/sicor/__init__.py'>
    In [2] used 204.0469 MiB RAM in 2.21s, peaked 0.00 MiB above current, total RAM usage 245.12 MiB


.. code:: python

    # README (!!!)
    # set up a working directory with all needed files (product, snr, ...)
    # load options, change needed parts
    # use [wrk_dir] as buffer dir
    # working directory 
    wrk_dir = "./enmap/"
    # if wrk dir doesn't exists -> bootsrap environment from repository
    if path.isdir(wrk_dir) is False:
        os.makedirs(wrk_dir, exist_ok=True)
        for fn in glob(path.join(sicor_dir,"tests", "data", "EnMAP","*.zip")):
            ZipFile(fn).extractall(wrk_dir)
        ZipFile(path.join(sicor_dir,"tests", "data", "EnMAP_Sensor","EnMAP_Level_1B_SNR.zip")).extractall(
        path.join(wrk_dir, "snr"))
    # replicate cli interface from bin/sicor_ac_EnMAP.py    
    args = SimpleNamespace(
        input=path.join(wrk_dir, "AlpineTest1_CWV2_SM1"),
        output=path.join(wrk_dir,"out_enmap"),
        snr_swir=path.join(wrk_dir, "snr", "SNR_D2.hdr"),
        snr_vnir=path.join(wrk_dir, "snr", "SNR_D1.hdr"),
        settings=path.join(sicor_dir, "options", "enmap_options.json")
    )
    
    # customize opzions (get path right)
    fn_aerosol = str(sicor_dir / "sicor" / "tables" / "linear_atm_functions_ncwv_5_npre_4_ncoz_2_ntmp_2_wvl_350.0_2550.0_1.00_pca.h5")
    fn_ch4 = str(sicor_dir / "sicor" / "tables" / "linear_atm_functions_ncwv_4_npre_2_ncoz_2_ntmp_1_nch4_4_wvl_350.0_2550.0_1.00_pca.h5")
    enmap_options = str(sicor_dir / "sicor/options/enmap_options.json")
    
    # adjust options
    options = get_options(enmap_options)
    options['EnMAP']['buffer_dir'] = wrk_dir
    for vv in options["RTFO"].values():
        vv["hash_formats"] = {'spr': '%.0f,', 'coz': '%.0f,', 'cwv': '%.0f,', 'tmp': '%0f,', 'tau_a': '%.2f,','vza': '%.0f,'}
    options["ECMWF"]["path_db"] = "./ecmwf"
    for name, val in options["RTFO"].items():
        if "aerosol" in name:
            val['atm_tables_fn'] = fn_aerosol
        if "ch4" in name:
            val['atm_tables_fn'] = fn_ch4


.. parsed-literal::

    In [3] used 0.9062 MiB RAM in 0.22s, peaked 0.00 MiB above current, total RAM usage 246.03 MiB


.. code:: python

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
    #options = get_options(args.settings)
    logger.info("Load settings: \n" + pprint.pformat(options))    


.. parsed-literal::

    15:10:55   INFO       <ipython-input-4-c513d5da092d> - <module>  : Sicor AC for EnMAP started.
    15:10:55   INFO       <ipython-input-4-c513d5da092d> - <module>  : Input = ./enmap/AlpineTest1_CWV2_SM1
    15:10:55   INFO       <ipython-input-4-c513d5da092d> - <module>  : Output = ./enmap/out_enmap
    15:10:55   INFO       <ipython-input-4-c513d5da092d> - <module>  : SNR VNIR = ./enmap/snr/SNR_D1.hdr
    15:10:55   INFO       <ipython-input-4-c513d5da092d> - <module>  : SNR SWIR = ./enmap/snr/SNR_D2.hdr
    15:10:55   INFO       <ipython-input-4-c513d5da092d> - <module>  : Settings = /misc/fluo6/andre/projekte/Sentinel2/py/sicor/options/enmap_options.json
    15:10:55   INFO       <ipython-input-4-c513d5da092d> - <module>  : Load settings: 
    {'ECMWF': {'conversion': {'coz': 71524.3,
                              'cwv': 1.0,
                              'spr': 0.01,
                              'tau_a': 1.0},
               'mapping': {'coz': 'fc_O3',
                           'cwv': 'fc_TCWV',
                           'spr': 'fc_SLP',
                           'tau_a': 'fc_total_AOT_550nm'},
               'max_delta_day': 10,
               'path_db': './ecmwf',
               'target_resolution': 20.0,
               'var2type': {'fc_black_carbon_AOT_550nm': 'aerosol_0',
                            'fc_dust_AOT_550nm': 'aerosol_3',
                            'fc_organic_matter_AOT_550nm': 'aerosol_2',
                            'fc_sea_salt_AOT_550nm': 'aerosol_1',
                            'fc_sulphate_AOT_550nm': 'aerosol_2'},
               'variables_aerosol': ['fc_total_AOT_550nm',
                                     'fc_sulphate_AOT_550nm',
                                     'fc_black_carbon_AOT_550nm',
                                     'fc_dust_AOT_550nm',
                                     'fc_organic_matter_AOT_550nm',
                                     'fc_sea_salt_AOT_550nm']},
     'EnMAP': {'aerosol_default': 'aerosol_0',
               'aerosol_model': 'ECMWF',
               'buffer_dir': './enmap/',
               'default_values': {'azi': 0.0,
                                  'ch4': 3.0,
                                  'coz': 400.0,
                                  'cwv': 20.0,
                                  'spr': 1020.0,
                                  'sza': 0.0,
                                  'tau_a': 0.2,
                                  'tmp': 0,
                                  'vza': 0.0},
               'keep_defaults_for': ['spr', 'cwv'],
               'lon_lat_smpl': [10, 10],
               'scene_detection_flags_to_process': [0.0],
               'solar_model': 'Thuillier2002',
               'use_only_rtfo': ['aerosol_0', 'ch4'],
               'wvl_rsp_sampling': 1.0},
     'RTFO': {'aerosol_0': {'atm_tables_fn': '/misc/fluo6/andre/projekte/Sentinel2/py/sicor/sicor/tables/linear_atm_functions_ncwv_5_npre_4_ncoz_2_ntmp_2_wvl_350.0_2550.0_1.00_pca.h5',
                            'dim_atm': ['spr', 'coz', 'cwv', 'tmp'],
                            'dim_scat': ['tau_a'],
                            'flag': 10,
                            'hash_formats': {'coz': '%.0f,',
                                             'cwv': '%.0f,',
                                             'spr': '%.0f,',
                                             'tau_a': '%.2f,',
                                             'tmp': '%0f,',
                                             'vza': '%.0f,'},
                            'only_toa': True,
                            'table_path': '/table_aerosol/type_0'},
              'aerosol_1': {'atm_tables_fn': '/misc/fluo6/andre/projekte/Sentinel2/py/sicor/sicor/tables/linear_atm_functions_ncwv_5_npre_4_ncoz_2_ntmp_2_wvl_350.0_2550.0_1.00_pca.h5',
                            'dim_atm': ['spr', 'coz', 'cwv', 'tmp'],
                            'dim_scat': ['tau_a'],
                            'flag': 10,
                            'hash_formats': {'coz': '%.0f,',
                                             'cwv': '%.0f,',
                                             'spr': '%.0f,',
                                             'tau_a': '%.2f,',
                                             'tmp': '%0f,',
                                             'vza': '%.0f,'},
                            'only_toa': True,
                            'table_path': '/table_aerosol/type_1'},
              'aerosol_2': {'atm_tables_fn': '/misc/fluo6/andre/projekte/Sentinel2/py/sicor/sicor/tables/linear_atm_functions_ncwv_5_npre_4_ncoz_2_ntmp_2_wvl_350.0_2550.0_1.00_pca.h5',
                            'dim_atm': ['spr', 'coz', 'cwv', 'tmp'],
                            'dim_scat': ['tau_a'],
                            'flag': 10,
                            'hash_formats': {'coz': '%.0f,',
                                             'cwv': '%.0f,',
                                             'spr': '%.0f,',
                                             'tau_a': '%.2f,',
                                             'tmp': '%0f,',
                                             'vza': '%.0f,'},
                            'only_toa': True,
                            'table_path': '/table_aerosol/type_2'},
              'aerosol_3': {'atm_tables_fn': '/misc/fluo6/andre/projekte/Sentinel2/py/sicor/sicor/tables/linear_atm_functions_ncwv_5_npre_4_ncoz_2_ntmp_2_wvl_350.0_2550.0_1.00_pca.h5',
                            'dim_atm': ['spr', 'coz', 'cwv', 'tmp'],
                            'dim_scat': ['tau_a'],
                            'flag': 10,
                            'hash_formats': {'coz': '%.0f,',
                                             'cwv': '%.0f,',
                                             'spr': '%.0f,',
                                             'tau_a': '%.2f,',
                                             'tmp': '%0f,',
                                             'vza': '%.0f,'},
                            'only_toa': True,
                            'table_path': '/table_aerosol/type_3'},
              'ch4': {'atm_tables_fn': '/misc/fluo6/andre/projekte/Sentinel2/py/sicor/sicor/tables/linear_atm_functions_ncwv_4_npre_2_ncoz_2_ntmp_1_nch4_4_wvl_350.0_2550.0_1.00_pca.h5',
                      'dim_atm': ['spr', 'coz', 'cwv', 'ch4'],
                      'dim_scat': ['tau_a'],
                      'flag': 10,
                      'hash_formats': {'coz': '%.0f,',
                                       'cwv': '%.0f,',
                                       'spr': '%.0f,',
                                       'tau_a': '%.2f,',
                                       'tmp': '%0f,',
                                       'vza': '%.0f,'},
                      'only_toa': True,
                      'table_path': '/table_aerosol/type_0_tmp_0'}},
     'output': [{'type': 'none'}],
     'processing': {'Exception': None,
                    'Exception_type': '',
                    'clear_fraction': None,
                    'interface': {'args': (), 'kwargs': {}},
                    'status': 1,
                    'tIO': 0.0,
                    'tRT': 0.0,
                    'uncertainties': {}}}


.. parsed-literal::

    In [4] used 0.1289 MiB RAM in 0.14s, peaked 0.00 MiB above current, total RAM usage 246.16 MiB


.. code:: python

    # config for call graphs
    from pycallgraph import PyCallGraph,Config
    from pycallgraph.output import GraphvizOutput
    from pycallgraph.output import PickleOutput
    from pycallgraph import GlobbingFilter
    
    def pcg(fname,max_depth=4,include=(), exclude=()):
        """
        To apply left to right, you might need this script:
            #!/bin/bash
            find ./ -maxdepth 1 -name "*.dot" -print \
            -exec sed -i 's/digraph G {/digraph G {rankdir=LR;/g' {} \; \
            -exec sed -i '/Generated by Python Call Graph v1.0.1/d' {} \; \
            -exec sed -i 's/digraph G {/digraph G {rankdir=LR;/g' {} \; \
            -exec sed -i 's/fontsize=10/fontsize=45/g' {} \;
    
            find ./ -maxdepth 1 -name "*.dot" -print -exec dot -Tpng {} -O \;
            for i in *.png ; do convert "$i" -resize 1500x "$i.jpg"  ; done    
        
        
        """
        config = Config(max_depth=max_depth,rankdir="LR",rotate=True)
        config.trace_filter = GlobbingFilter(include=include, exclude=exclude)
        outp = [GraphvizOutput(output_file='%s.png' % fname,output_type="png",font_size=34),
                GraphvizOutput(output_file='%s.dot' % fname,output_type="dot",font_size=34)
               ]
        return PyCallGraph(output=outp, config=config)



.. parsed-literal::

    In [5] used 0.0039 MiB RAM in 0.15s, peaked 0.00 MiB above current, total RAM usage 246.16 MiB


.. code:: python

    if False:  # decite to run callgrapg or not
        for run in ("_1st", "_2nd"):  # two passes, to cover buffer table generation
            with pcg(fname=path.join(wrk_dir,"sicor_enmap_call_graph%s" % run),max_depth=6,
                     include=("sicor.*"), exclude=("ModuleSpec*", "_handle_fromlist*", "_find_and_load*", "_gcd_import*", "_ModuleLock*","cb")):
                enmap_l1b = L1B_Reader(logger=logger).read_inputdata(
                    root_dir=args.input,
                    observation_time=datetime(2015, 12, 7, 10),
                    lon_lat_smpl=options["EnMAP"]['lon_lat_smpl'],
                    snr_vnir=args.snr_vnir,
                    snr_swir=args.snr_swir)    
                enmap_l2a_sens_geo, state, fits = sicor_ac_enmap(enmap_l1b=enmap_l1b,options=options,logger=logger, debug=True)
    else:
        enmap_l1b = L1B_Reader(logger=logger).read_inputdata(
            root_dir=args.input,
            observation_time=datetime(2015, 12, 7, 10),
            lon_lat_smpl=options["EnMAP"]['lon_lat_smpl'],
            snr_vnir=args.snr_vnir,
            snr_swir=args.snr_swir)    
        enmap_l2a_sens_geo, state, fits = sicor_ac_enmap(enmap_l1b=enmap_l1b,options=options,logger=logger, debug=True)


.. parsed-literal::

    15:12:06   INFO       metadata   - read_metadata: Load data for: detector1
    15:12:06   INFO       metadata   - read_metadata: Load data for: detector2


.. parsed-literal::

    2017/09/26 15:12:07:   Converting DN values to radiance for VNIR detector...
    2017/09/26 15:12:07:   Converting DN values to radiance for SWIR detector...


.. parsed-literal::

    15:12:07   INFO       reader     - read_inputdata: Compute SNR for vnir: ./enmap/snr/SNR_D1.hdr
    15:12:07   INFO       metadata   - calc_snr_vnir: Compute snr for: VNIR using: ./enmap/snr/SNR_D1.hdr
    15:12:07   INFO       reader     - read_inputdata: Compute SNR for swir: ./enmap/snr/SNR_D2.hdr
    15:12:07   INFO       metadata   - calc_snr_swir: Compute snr for: SWIR using: ./enmap/snr/SNR_D2.hdr
    15:12:07   INFO       sicor_enmap - load_fos_enmap: Try to read from: ./enmap/aerosol_0_ch4_45cbf70ec42e57f4fb582c57eec1e7648946c911.pkl.zip
    15:12:21   INFO       sicor_enmap - load_tables_from_buffer_file: Restore: aerosol_0
    15:12:21   INFO       sicor_enmap - load_tables_from_buffer_file: Restore: ch4
    15:12:21   INFO       sicor_enmap - sicor_ac_enmap: Convert radiance to reflectance
    15:12:21   INFO       sicor_enmap - get_atmospheric_state: {'fo_instances': {'aerosol_0': {'flag': 10}, 'ch4': {'flag': 10}}, 'atm_fields': ['spr', 'ch4', 'tau_a', 'coz', 'tmp', 'cwv'], 'pt_names': ['spr', 'coz', 'cwv', 'tmp', 'tau_a', 'vza', 'sza', 'azi', 'ch4'], 'pt_indexes': {'aerosol_0': array([0, 1, 2, 3, 4, 5, 6, 7]), 'ch4': array([0, 1, 2, 8, 4, 5, 6, 7])}}
    15:12:21   INFO       sicor_enmap - get_atmospheric_state: Set defaults for vnir: spr = 1020.00
    15:12:21   INFO       sicor_enmap - get_atmospheric_state: Set defaults for swir: spr = 1020.00
    15:12:21   INFO       sicor_enmap - get_atmospheric_state: Set defaults for vnir: coz = 400.00
    15:12:21   INFO       sicor_enmap - get_atmospheric_state: Set defaults for swir: coz = 400.00
    15:12:21   INFO       sicor_enmap - get_atmospheric_state: Set defaults for vnir: cwv = 20.00
    15:12:21   INFO       sicor_enmap - get_atmospheric_state: Set defaults for swir: cwv = 20.00
    15:12:21   INFO       sicor_enmap - get_atmospheric_state: Set defaults for vnir: tmp = 0.00
    15:12:21   INFO       sicor_enmap - get_atmospheric_state: Set defaults for swir: tmp = 0.00
    15:12:21   INFO       sicor_enmap - get_atmospheric_state: Set defaults for vnir: tau_a = 0.20
    15:12:21   INFO       sicor_enmap - get_atmospheric_state: Set defaults for swir: tau_a = 0.20
    15:12:21   INFO       sicor_enmap - get_atmospheric_state: Set defaults for vnir: ch4 = 3.00
    15:12:21   INFO       sicor_enmap - get_atmospheric_state: Set defaults for swir: ch4 = 3.00
    15:12:21   INFO       sicor_enmap - get_atmospheric_state: Set defaults for vnir: vza = 7.80
    15:12:21   INFO       sicor_enmap - get_atmospheric_state: Set defaults for swir: vza = 7.80
    15:12:21   INFO       sicor_enmap - get_atmospheric_state: Set defaults for vnir: sza = 34.60
    15:12:21   INFO       sicor_enmap - get_atmospheric_state: Set defaults for swir: sza = 34.60
    15:12:21   INFO       sicor_enmap - get_atmospheric_state: Set defaults for vnir: azi = 75.10
    15:12:21   INFO       sicor_enmap - get_atmospheric_state: Set defaults for swir: azi = 75.10
    15:12:21   INFO       sicor_enmap - determine_pixels_to_be_processed: Included flag: 0.0 for: vnir
    15:12:21   INFO       sicor_enmap - determine_pixels_to_be_processed: Included flag: 0.0 for: swir
    15:12:21   INFO       sicor_enmap - determine_pixels_to_be_processed: #### insert dummy ac map, remove in future ####
    15:12:21   INFO       sicor_enmap - determine_pixels_to_be_processed: #### insert dummy ac map, remove in future ####
    15:12:21   INFO       sicor_enmap - determine_pixels_to_be_processed: #### insert dummy ac map, remove in future ####
    15:12:21   INFO       sicor_enmap - get_state_from_ECMWF: Get ECMWF data for detector: vnir
    15:12:21   INFO       sicor_enmap - get_state_from_ECMWF: ECMWF for fc_total_AOT_550nm not present.
    15:12:21   INFO       sicor_enmap - get_state_from_ECMWF: ECMWF for fc_O3 not present.
    15:12:21   INFO       sicor_enmap - get_state_from_ECMWF: Get ECMWF data for detector: swir
    15:12:21   INFO       sicor_enmap - get_state_from_ECMWF: ECMWF for fc_total_AOT_550nm not present.
    15:12:21   INFO       sicor_enmap - get_state_from_ECMWF: ECMWF for fc_O3 not present.
    15:12:21   INFO       sicor_enmap - sicor_ac_enmap: Determine aerosol type from ECMWF
    15:12:21   ERROR      sicor_enmap - get_aerosol_model_from_ecmwf: ECMWF data for aerosol not found, continue with default value: aerosol_0 
    Traceback (most recent call last):
      File "/misc/fluo6/andre/projekte/Sentinel2/py/sicor/sicor/sicor_enmap.py", line 336, in get_aerosol_model_from_ecmwf
        var_date=enmap_l1b.meta.observation_datetime)(
      File "/misc/fluo6/andre/projekte/Sentinel2/py/sicor/sicor/ECMWF/ECMWF.py", line 591, in __init__
        raise FileNotFoundError(self.fn)
    FileNotFoundError: ./ecmwf/fc_total_AOT_550nm/2015/12/20151207_fc_total_AOT_550nm.h5
    15:12:21   INFO       sicor_enmap - get_aerosol_model_from_ecmwf: Chosen aerosol model from ECMWF: aerosol_0
    15:12:21   INFO       sicor_enmap - sicor_ac_enmap: ####### Remove #############
    15:12:21   INFO       sicor_enmap - sicor_ac_enmap: ####################
    15:12:21   INFO       sicor_enmap - sicor_ac_enmap: Estimate ch4 from data.
    15:12:21   INFO       sicor_enmap - optimize_inverse_table: Reduce azi -> 75.1
    15:12:21   INFO       sicor_enmap - optimize_inverse_table: Reduce coz -> 400.0
    15:12:21   INFO       sicor_enmap - optimize_inverse_table: Reduce vza -> 7.8
    15:12:21   INFO       sicor_enmap - optimize_inverse_table: Reduce tau_a -> 0.2
    15:12:21   INFO       sicor_enmap - optimize_inverse_table: Reduce spr -> 1020.0
    15:12:21   INFO       sicor_enmap - optimize_inverse_table: Reduce cwv -> 20.0
    15:12:21   INFO       sicor_enmap - optimize_inverse_table: Reduce tmp -> 0.0
    100%|██████████| 1000/1000 [00:07<00:00, 137.65it/s]
    15:12:29   INFO       sicor_enmap - sicor_ac_enmap: Put fg to state for: ch4
    15:12:29   INFO       inpaint    - inpaint   : bad/total ratio: 0.08880
    15:12:29   INFO       inpaint    - inpaint   : (1, 45560)
    15:12:29   INFO       inpaint    - inpaint   : Splitting array into 1^2 parts.
    15:12:29   INFO       inpaint    - inpaint   : bad/total ratio: 0.08880
    15:12:29   INFO       inpaint    - inpaint   : bad/total ratio: 0.00000
    15:12:29   INFO       inpaint    - inpaint   : Inpainting runtime: 0.29s
     10%|█         | 101/1000 [02:43<23:04,  1.54s/it]
      0%|          | 0/1000 [00:00<?, ?it/s][A
    
    
    
      0%|          | 1/1000 [00:01<26:55,  1.62s/it][A
    
    
    
      0%|          | 2/1000 [00:03<26:51,  1.61s/it][A
    
    
    
      0%|          | 3/1000 [00:04<27:21,  1.65s/it][A
    
    
    
     10%|█         | 101/1000 [02:46<24:17,  1.62s/it]15:18:02   INFO       sicor_enmap - make_ac   : AC for detector: vnir
    15:18:02   INFO       sicor_enmap - make_ac   : Perform columnwise ac
    
      0%|          | 0/1000 [00:00<?, ?it/s][A
      0%|          | 1/1000 [00:01<30:41,  1.84s/it][A
      1%|          | 11/1000 [00:01<21:19,  1.29s/it][A
      2%|▏         | 21/1000 [00:02<14:49,  1.10it/s][A
      3%|▎         | 31/1000 [00:02<10:19,  1.56it/s][A
      4%|▍         | 40/1000 [00:02<07:12,  2.22it/s][A
      5%|▌         | 50/1000 [00:02<05:02,  3.14it/s][A
      6%|▌         | 59/1000 [00:02<03:33,  4.41it/s][A
      7%|▋         | 69/1000 [00:02<02:30,  6.18it/s][A
      8%|▊         | 78/1000 [00:02<01:47,  8.56it/s][A
      9%|▉         | 88/1000 [00:02<01:17, 11.76it/s][A
     10%|▉         | 97/1000 [00:02<00:57, 15.78it/s][A
     11%|█         | 106/1000 [00:03<00:44, 20.15it/s][A
     12%|█▏        | 115/1000 [00:03<00:33, 26.25it/s][A
     12%|█▎        | 125/1000 [00:03<00:26, 33.33it/s][A
     14%|█▎        | 135/1000 [00:03<00:21, 41.15it/s][A
     14%|█▍        | 144/1000 [00:03<00:17, 49.15it/s][A
     15%|█▌        | 154/1000 [00:03<00:14, 57.06it/s][A
     16%|█▋        | 164/1000 [00:03<00:13, 64.22it/s][A
     17%|█▋        | 173/1000 [00:03<00:11, 69.65it/s][A
     18%|█▊        | 182/1000 [00:03<00:10, 74.56it/s][A
     19%|█▉        | 191/1000 [00:04<00:10, 78.27it/s][A
     20%|██        | 201/1000 [00:04<00:09, 81.72it/s][A
     21%|██        | 210/1000 [00:04<00:09, 83.97it/s][A
     22%|██▏       | 220/1000 [00:04<00:09, 85.77it/s][A
     23%|██▎       | 230/1000 [00:04<00:08, 87.33it/s][A
     24%|██▍       | 240/1000 [00:04<00:08, 88.23it/s][A
     25%|██▌       | 250/1000 [00:04<00:08, 88.35it/s][A
     26%|██▌       | 262/1000 [00:04<00:07, 94.78it/s][A
     28%|██▊       | 278/1000 [00:04<00:06, 106.92it/s][A
     29%|██▉       | 294/1000 [00:04<00:06, 117.32it/s][A
     31%|███       | 310/1000 [00:05<00:05, 126.42it/s][A
     32%|███▎      | 325/1000 [00:05<00:05, 132.57it/s][A
     34%|███▍      | 341/1000 [00:05<00:04, 137.83it/s][A
     36%|███▌      | 357/1000 [00:05<00:04, 142.70it/s][A
     37%|███▋      | 373/1000 [00:05<00:04, 146.04it/s][A
     39%|███▉      | 388/1000 [00:05<00:04, 130.99it/s][A
     40%|████      | 402/1000 [00:05<00:05, 116.15it/s][A
     42%|████▏     | 415/1000 [00:05<00:05, 106.79it/s][A
     43%|████▎     | 427/1000 [00:06<00:05, 100.46it/s][A
     44%|████▍     | 438/1000 [00:06<00:05, 97.61it/s] [A
     45%|████▍     | 449/1000 [00:06<00:05, 96.25it/s][A
     46%|████▌     | 459/1000 [00:06<00:05, 94.73it/s][A
     47%|████▋     | 469/1000 [00:06<00:05, 91.56it/s][A
     48%|████▊     | 479/1000 [00:06<00:05, 89.32it/s][A
     49%|████▉     | 489/1000 [00:06<00:05, 86.13it/s][A
     50%|████▉     | 498/1000 [00:06<00:05, 87.17it/s][A
     51%|█████     | 508/1000 [00:07<00:05, 88.63it/s][A
     52%|█████▏    | 518/1000 [00:07<00:05, 89.67it/s][A
     53%|█████▎    | 528/1000 [00:07<00:05, 90.43it/s][A
     54%|█████▍    | 538/1000 [00:07<00:05, 90.85it/s][A
     55%|█████▍    | 548/1000 [00:07<00:04, 91.29it/s][A
     56%|█████▌    | 558/1000 [00:07<00:04, 91.59it/s][A
     57%|█████▋    | 568/1000 [00:07<00:04, 90.83it/s][A
     58%|█████▊    | 578/1000 [00:07<00:04, 87.60it/s][A
    100%|██████████| 1000/1000 [00:12<00:00, 80.95it/s]
    15:18:14   INFO       sicor_enmap - make_ac   : AC for detector: swir
    15:18:14   INFO       sicor_enmap - make_ac   : Perform columnwise ac
    100%|██████████| 1000/1000 [00:10<00:00, 98.25it/s]


.. parsed-literal::

    In [6] used 3347.6133 MiB RAM in 378.27s, peaked 57.68 MiB above current, total RAM usage 3593.78 MiB


.. code:: python

    # run this if you want to generate call graphs
    #convert to better graphics
    %%bash
    cd ./enmap/
    find ./ -maxdepth 1 -name "*.dot" -print \
    -exec sed -i 's/digraph G {/digraph G {rankdir=LR;/g' {} \; \
    -exec sed -i '/Generated by Python Call Graph v1.0.1/d' {} \; \
    -exec sed -i 's/digraph G {/digraph G {rankdir=LR;/g' {} \; \
    -exec sed -i 's/fontsize=10/fontsize=45/g' {} \;
    
    find ./ -maxdepth 1 -name "*.dot" -print -exec dot -Tpng {} -O \;
    for i in *.png ; do convert "$i" -resize 3000x "$i.jpg"  ; done

.. code:: python

    from IPython.display import Image
    #Image(filename='enmap/cg/sicor_enmap_call_graph_1st.dot.png.jpg')
    Image(filename='../docs/examples/sicor_ac_EnMAP/sicor_ac_EnMAP_10_0.jpeg')




.. image:: examples/sicor_ac_EnMAP/sicor_ac_EnMAP_9_0.jpeg


.. parsed-literal::

    In [7] used 0.0039 MiB RAM in 0.19s, peaked 0.00 MiB above current, total RAM usage 3593.78 MiB


.. code:: python

    from IPython.display import Image
    #Image(filename='enmap/cg/sicor_enmap_call_graph_2nd.dot.png.jpg')
    Image(filename='./../docs/examples/sicor_ac_EnMAP/sicor_ac_EnMAP_9_0.jpeg')




.. image:: examples/sicor_ac_EnMAP/sicor_ac_EnMAP_10_0.jpeg


.. parsed-literal::

    In [8] used 0.0039 MiB RAM in 0.19s, peaked 0.00 MiB above current, total RAM usage 3593.79 MiB


For debugging and development, exposing the sicor\_ac\_enmap function in
a cell:

.. code:: python

    debug = True


.. parsed-literal::

    In [11] used 0.0625 MiB RAM in 0.15s, peaked 0.00 MiB above current, total RAM usage 6483.13 MiB


.. code:: python

    enmap_l1b = L1B_Reader(logger=logger).read_inputdata(
        root_dir=args.input,
        observation_time=datetime(2015, 12, 7, 10),
        lon_lat_smpl=options["EnMAP"]['lon_lat_smpl'],
        snr_vnir=args.snr_vnir,
        snr_swir=args.snr_swir)    
    
    
    #enmap_l2a_sens_geo, state = sicor_ac_enmap(enmap_l1b=enmap_l1b,options=options,logger=logger)
    #def sicor_ac_enmap(enmap_l1b: EnMAPL1Product_SensorGeo, options: dict, logger=None, debug=False) -> EnMAPL1Product_SensorGeo:
    if True:
        
        options["EnMAP"]["keep_defaults_for"] = ["spr", "cwv"]
    
        import logging
        import hashlib
        from datetime import datetime
        import numpy as np
        from os import path
        import pickle
        import gzip
        from sicor.Tools import SolarIrradiance
        from tqdm import tqdm
        from scipy.interpolate import griddata
        from sklearn.decomposition import PCA
        from itertools import product
    
        from enpt.model.images import EnMAPL1Product_SensorGeo
    
        from sicor.AC.RtFo import RtFo, sat
        from sicor.AC.ACG import get_pt_names_and_indexes
        from sicor.ECMWF import ECMWF_variable
        from sicor.Tools import inpaint    
        
        
        """Atmospheric correction for EnMAP Level-1B products.
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
                "detector_name": "vnir", "wvl_center": 960.0, "wvl_bands_intervall": [2, 2],
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
            },
    
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
                    
        # full specral fit, per column, per pixel
        fit_options = {
            "cwv":{
                "sensors":sensors, "state":state,
                "enmap_l1b":enmap_l1b, "detector_name":"vnir", "options":options,"fo":fos["aerosol_0"],
                "optimize_dims_atm": ("cwv",), "wvl_center":950.0, "wvl_bands_intervall":(5,5),
                "reduced_luts": {"azi":0.0,"coz":350.0,"vza":0.0,"tau_a":0.2,"tmp":0},
                "pt_index": options["settings"]['pt_indexes']['aerosol_0'],"debug":debug},
            "ch4":{
                "sensors":sensors, "state":state,
                "enmap_l1b":enmap_l1b, "detector_name": "swir", "options":options,"fo":fos["ch4"],
                "optimize_dims_atm": ("ch4",),"wvl_center":2380.0,"wvl_bands_intervall":(15,7),
                "reduced_luts":{"azi":0.0,"coz":350.0,"vza":0.0,"tau_a":0.2,"cwv":20.0,"tmp":0},
                "pt_index":options["settings"]['pt_indexes']['ch4'],"debug":debug
            }
        }
        fits = {fit:optimize(**opts) for fit,opts in fit_options.items()}
    
        # perform ac
        #make_ac(enmap_l1b, state, options, fos, logger)
    
        #return enmap_l1b, state


.. parsed-literal::

    15:22:15   INFO       metadata   - read_metadata: Load data for: detector1
    15:22:15   INFO       metadata   - read_metadata: Load data for: detector2


.. parsed-literal::

    2017/09/26 15:22:16:   Converting DN values to radiance for VNIR detector...
    2017/09/26 15:22:16:   Converting DN values to radiance for SWIR detector...


.. parsed-literal::

    15:22:16   INFO       reader     - read_inputdata: Compute SNR for vnir: ./enmap/snr/SNR_D1.hdr
    15:22:16   INFO       metadata   - calc_snr_vnir: Compute snr for: VNIR using: ./enmap/snr/SNR_D1.hdr
    15:22:16   INFO       reader     - read_inputdata: Compute SNR for swir: ./enmap/snr/SNR_D2.hdr
    15:22:16   INFO       metadata   - calc_snr_swir: Compute snr for: SWIR using: ./enmap/snr/SNR_D2.hdr
    15:22:17   INFO       sicor_enmap - load_fos_enmap: Try to read from: ./enmap/aerosol_0_ch4_45cbf70ec42e57f4fb582c57eec1e7648946c911.pkl.zip
    15:22:31   INFO       sicor_enmap - load_tables_from_buffer_file: Restore: aerosol_0
    15:22:31   INFO       sicor_enmap - load_tables_from_buffer_file: Restore: ch4
    15:22:31   INFO       <ipython-input-12-d790180bb4d5> - <module>  : Convert radiance to reflectance
    15:22:31   INFO       sicor_enmap - get_atmospheric_state: {'fo_instances': {'aerosol_0': {'flag': 10}, 'ch4': {'flag': 10}}, 'atm_fields': ['spr', 'ch4', 'tau_a', 'coz', 'tmp', 'cwv'], 'pt_names': ['spr', 'coz', 'cwv', 'tmp', 'tau_a', 'vza', 'sza', 'azi', 'ch4'], 'pt_indexes': {'aerosol_0': array([0, 1, 2, 3, 4, 5, 6, 7]), 'ch4': array([0, 1, 2, 8, 4, 5, 6, 7])}}
    15:22:31   INFO       sicor_enmap - get_atmospheric_state: Set defaults for vnir: spr = 1020.00
    15:22:31   INFO       sicor_enmap - get_atmospheric_state: Set defaults for swir: spr = 1020.00
    15:22:31   INFO       sicor_enmap - get_atmospheric_state: Set defaults for vnir: coz = 400.00
    15:22:31   INFO       sicor_enmap - get_atmospheric_state: Set defaults for swir: coz = 400.00
    15:22:31   INFO       sicor_enmap - get_atmospheric_state: Set defaults for vnir: cwv = 20.00
    15:22:31   INFO       sicor_enmap - get_atmospheric_state: Set defaults for swir: cwv = 20.00
    15:22:31   INFO       sicor_enmap - get_atmospheric_state: Set defaults for vnir: tmp = 0.00
    15:22:31   INFO       sicor_enmap - get_atmospheric_state: Set defaults for swir: tmp = 0.00
    15:22:31   INFO       sicor_enmap - get_atmospheric_state: Set defaults for vnir: tau_a = 0.20
    15:22:31   INFO       sicor_enmap - get_atmospheric_state: Set defaults for swir: tau_a = 0.20
    15:22:31   INFO       sicor_enmap - get_atmospheric_state: Set defaults for vnir: ch4 = 3.00
    15:22:31   INFO       sicor_enmap - get_atmospheric_state: Set defaults for swir: ch4 = 3.00
    15:22:31   INFO       sicor_enmap - get_atmospheric_state: Set defaults for vnir: vza = 7.80
    15:22:31   INFO       sicor_enmap - get_atmospheric_state: Set defaults for swir: vza = 7.80
    15:22:31   INFO       sicor_enmap - get_atmospheric_state: Set defaults for vnir: sza = 34.60
    15:22:31   INFO       sicor_enmap - get_atmospheric_state: Set defaults for swir: sza = 34.60
    15:22:31   INFO       sicor_enmap - get_atmospheric_state: Set defaults for vnir: azi = 75.10
    15:22:31   INFO       sicor_enmap - get_atmospheric_state: Set defaults for swir: azi = 75.10
    15:22:31   INFO       sicor_enmap - determine_pixels_to_be_processed: Included flag: 0.0 for: vnir
    15:22:31   INFO       sicor_enmap - determine_pixels_to_be_processed: Included flag: 0.0 for: swir
    15:22:31   INFO       sicor_enmap - determine_pixels_to_be_processed: #### insert dummy ac map, remove in future ####
    15:22:31   INFO       sicor_enmap - determine_pixels_to_be_processed: #### insert dummy ac map, remove in future ####
    15:22:31   INFO       sicor_enmap - determine_pixels_to_be_processed: #### insert dummy ac map, remove in future ####
    15:22:31   INFO       sicor_enmap - get_state_from_ECMWF: Get ECMWF data for detector: vnir
    15:22:31   INFO       sicor_enmap - get_state_from_ECMWF: ECMWF for fc_total_AOT_550nm not present.
    15:22:31   INFO       sicor_enmap - get_state_from_ECMWF: ECMWF for fc_O3 not present.
    15:22:31   INFO       sicor_enmap - get_state_from_ECMWF: Get ECMWF data for detector: swir
    15:22:31   INFO       sicor_enmap - get_state_from_ECMWF: ECMWF for fc_total_AOT_550nm not present.
    15:22:31   INFO       sicor_enmap - get_state_from_ECMWF: ECMWF for fc_O3 not present.
    15:22:31   INFO       <ipython-input-12-d790180bb4d5> - <module>  : Use given aerosol type: aerosol_0
    15:22:31   INFO       <ipython-input-12-d790180bb4d5> - <module>  : ####### Remove #############
    15:22:31   INFO       <ipython-input-12-d790180bb4d5> - <module>  : ####################
    15:22:31   INFO       <ipython-input-12-d790180bb4d5> - <module>  : Estimate ch4 from data.
    15:22:31   INFO       sicor_enmap - optimize_inverse_table: Reduce azi -> 75.1
    15:22:31   INFO       sicor_enmap - optimize_inverse_table: Reduce coz -> 400.0
    15:22:31   INFO       sicor_enmap - optimize_inverse_table: Reduce vza -> 7.8
    15:22:31   INFO       sicor_enmap - optimize_inverse_table: Reduce tau_a -> 0.2
    15:22:31   INFO       sicor_enmap - optimize_inverse_table: Reduce spr -> 1020.0
    15:22:31   INFO       sicor_enmap - optimize_inverse_table: Reduce cwv -> 20.0
    15:22:31   INFO       sicor_enmap - optimize_inverse_table: Reduce tmp -> 0.0
    100%|██████████| 1000/1000 [00:06<00:00, 151.09it/s]
    15:22:38   INFO       <ipython-input-12-d790180bb4d5> - <module>  : Put fg to state for: ch4
    15:22:38   INFO       inpaint    - inpaint   : bad/total ratio: 0.08880
    15:22:38   INFO       inpaint    - inpaint   : (1, 45560)
    15:22:38   INFO       inpaint    - inpaint   : Splitting array into 1^2 parts.
    15:22:38   INFO       inpaint    - inpaint   : bad/total ratio: 0.08880
    15:22:38   INFO       inpaint    - inpaint   : bad/total ratio: 0.00000
    15:22:38   INFO       inpaint    - inpaint   : Inpainting runtime: 0.01s
     10%|█         | 101/1000 [03:07<26:19,  1.76s/it]
      0%|          | 0/1000 [00:00<?, ?it/s][A
    
    
    
     10%|█         | 101/1000 [03:04<26:46,  1.79s/it]

.. parsed-literal::

    In [12] used 2845.3008 MiB RAM in 398.22s, peaked 75.59 MiB above current, total RAM usage 9328.43 MiB


.. code:: python

    i1,i2 = 5, 7
    nn = len(fits.keys()),3
    fig = plt.figure(figsize=[10*ni for ni in nn][::-1])
    aspect = enmap_l1b.vnir.data.shape[1] / enmap_l1b.vnir.data.shape[0]
    for ifit,(var,fit) in enumerate(fits.items()):
        
        detector = getattr(enmap_l1b,fit_options[var]['detector_name'])
        meta = getattr(enmap_l1b.meta,fit_options[var]['detector_name'])
        
        ax = plt.subplot2grid(nn, (ifit, 0))
        ax.imshow(fit["results"][:,:,0],aspect=aspect)
        
        ax = plt.subplot2grid(nn, (ifit, 1))
        ax.imshow(fit["residuals"][:,:],aspect=aspect)  # use this to filter results
        
         #fo fit vs data
        ax = plt.subplot2grid(nn, (ifit, 2))
        ax.plot(
            meta.wvl_center[fit['wvl_sel']], 
            fit["spectra"][i1,i2,:],label="fo fit result %s: %.2f (rmse:%.4f)" % (
                var,fit["results"][i1, i2,0],fit["residuals"][i1, i2]))
        ax.plot(
            meta.wvl_center[fit['wvl_sel']], 
            detector.data[i1,i2,fit['wvl_sel']],"r",label="data")
        _ = plt.legend()   



.. image:: examples/sicor_ac_EnMAP/sicor_ac_EnMAP_14_0.png

.. parsed-literal::

    In [13] used 7.4883 MiB RAM in 1.56s, peaked 0.00 MiB above current, total RAM usage 9335.92 MiB

