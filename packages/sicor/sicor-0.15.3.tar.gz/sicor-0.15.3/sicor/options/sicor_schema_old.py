"""Definition of sicor options schema (as used by cerberus library)."""
sicor_schema = {
    'ECMWF': {  # All options related to the download and loading of ECMWF products.
        'type': 'dict',
        'schema': {
            'path_db': {  # Path to ECMWF database (folder structure) on disk.
                          # An example is given in  [repo]/sicor/tests/data/ecmwf/ecmwf.zip.
                          # Download products with: [repo]/sicor/bin/sicor_ecmwf.py
                "type": "string",
                "required": True,
                "existing_path": True  # This path should exist.
            },
            'target_resolution': {  # Target spatial sampling in meter, e.g.: [20.0]
                "type": "float",
                "required": True
            },
            "variables_aerosol": {  # List of ecmwf products which are treated as aerosol forecasts.
                                    # These are also names in the root of the ecmwf database folder structure,
                                    # e.g.: ["fc_total_AOT_550nm", ... , "fc_sea_salt_AOT_550nm"]
                "type": "list",
                "required": True,
                'schema': {'type': 'string'}
            },
            'var2type': {  # Mapping dictionary with key value pairs which map ecmwf product names to
                           # aerosol names in the look up tables, e.g.: {"fc_organic_matter_AOT_550nm": "aerosol_2"}
                "type": "dict",
                "required": True,
                'keyschema': {'type': 'string', 'regex': '[a-zA-Z0-9_]+'}
            },
            'mapping': {  # Mapping dictionary with key value pairs which maps internal look up table
                          # variable names to ecmwf products, e.g.: {"tau_a": "fc_total_AOT_550nm"}
                "type": "dict",
                "required": False
            },
            'conversion': {  # Conversion factor from ecmwf units to look-up table units, e.g. {"coz": 71524.3}
                "type": "dict",
                "required": False,
                "valueschema": {"type": "float"}
            }
        }  # end of 'ECMWF/schema'
    },  # end of 'ECMWF'
    "EnMAP": {
        'type': 'dict',
        'schema': {
            "solar_model": {
                "type": "string", "required": True},
            "wvl_rsp_sampling": {"type": "float", "required": True},
            "buffer_dir": {"type": "string", "required": True, "existing_path": True},
            "keep_defaults_for": {"type": "list", "required": True, "schema": {
                "type": "string", "allowed": [
                    "spr", "coz", "cwv", "tmp", "tau_a", "vza", "sza", "azi"
                ]}},
            "default_values": {"type": "dict", "required": True,
                               'allow_unknown': False,
                               "schema": {par: {"type": "float", "required": True} for par in [
                                   "spr", "coz", "cwv", "tmp", "tau_a", "vza", "sza", "azi", "ch4"
                               ]}},
            "lon_lat_smpl": {"type": "list", "schema": {"type": "integer"}, "minlength": 2, "maxlength": 2},
            "aerosol_model": {"type": 'string', 'required': True},
            "scene_detection_flags_to_process": {"type": "list", "required": True, "allowed": [0.0]},
            "use_only_rtfo": {"type": "list", "schema": {"type": "string"}},
            "aerosol_default": {"type": "string"},
        }
    },
    'output': {'type': 'list', 'required': True,
               'schema': {'type': 'dict',
                          'schema': {'type': {'type': 'string', 'required': True,
                                              'allowed': ['L2A', 'metadata', 'rgb_jpeg', 'none']}}}}
}
