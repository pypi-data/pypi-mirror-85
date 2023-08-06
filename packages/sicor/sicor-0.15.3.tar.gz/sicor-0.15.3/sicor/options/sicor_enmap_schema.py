"""Definition of sicor enmap options schema (as used by cerberus library)."""
sicor_enmap_schema = {
    "EnMAP": {
        "type": "dict",
        "schema": {
            "FO_settings": {
                "type": "dict",
                "schema": {
                    "aot": {
                        "type": "float",
                        "required": True
                    }
                }
            },
            "Retrieval": {
                "type": "dict",
                "schema": {
                    "fn_LUT": {
                        "type": "string",
                        "required": True,
                        "existing_path": True
                    },
                    "fast": {
                        "type": "boolean",
                        "required": True
                    },
                    "ice": {
                        "type": "boolean",
                        "required": True
                    },
                    "cpu": {
                        "type": "integer",
                        "required": True
                    },
                    "disable_progressbars": {
                        "type": "boolean",
                        "required": True
                    },
                    "segmentation": {
                        "type": "boolean",
                        "required": True
                    },
                    "n_pca": {
                        "type": "integer",
                        "required": True
                    },
                    "segs": {
                        "type": "integer",
                        "required": True
                    }
                }
            }
        }
    }
}
