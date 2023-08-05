VALIDATE_TASK_SCHEMA = '''{
    "additionalProperties": false,
    "properties": {
        "clusters": {
            "items": {
                "additionalProperties": false,
                "properties": {
                    "performer_key": {
                        "maxLength": 1024,
                        "minLength": 1,
                        "type": "string"
                    },
                    "points_keys": {
                        "items": {
                            "maxLength": 1024,
                            "minLength": 1,
                            "type": "string"
                        },
                        "maxItems": 9000,
                        "minItems": 1,
                        "type": "array"
                    },
                    "representer_key": {
                        "maxLength": 1024,
                        "minLength": 1,
                        "type": "string"
                    }
                },
                "required": [
                    "performer_key",
                    "points_keys"
                ],
                "type": "object"
            },
            "maxItems": 9000,
            "minItems": 0,
            "type": "array"
        },
        "performers": {
            "items": {
                "additionalProperties": false,
                "properties": {
                    "cost_per_meter": {
                        "default": 0,
                        "format": "double",
                        "minimum": 0,
                        "type": "number"
                    },
                    "cost_per_minute": {
                        "default": 0,
                        "format": "double",
                        "minimum": 0,
                        "type": "number"
                    },
                    "home_location": {
                        "additionalProperties": false,
                        "properties": {
                            "arrival_duration": {
                                "default": 0,
                                "format": "int32",
                                "maximum": 1440,
                                "minimum": 0,
                                "type": "integer"
                            },
                            "departure_duration": {
                                "default": 0,
                                "format": "int32",
                                "maximum": 1440,
                                "minimum": 0,
                                "type": "integer"
                            },
                            "latitude": {
                                "format": "double",
                                "maximum": 90,
                                "minimum": -90,
                                "type": "number"
                            },
                            "longitude": {
                                "format": "double",
                                "maximum": 180,
                                "minimum": -180,
                                "type": "number"
                            }
                        },
                        "required": [
                            "latitude",
                            "longitude"
                        ],
                        "type": "object"
                    },
                    "key": {
                        "maxLength": 1024,
                        "minLength": 1,
                        "type": "string"
                    },
                    "limits": {
                        "additionalProperties": false,
                        "nullable": false,
                        "properties": {
                            "max_points": {
                                "default": 1,
                                "format": "int32",
                                "maximum": 7000,
                                "minimum": 1,
                                "type": "integer"
                            },
                            "min_points": {
                                "default": 1,
                                "format": "int32",
                                "maximum": 7000,
                                "minimum": 1,
                                "type": "integer"
                            }
                        },
                        "type": "object"
                    },
                    "transport_type": {
                        "default": "CAR",
                        "enum": [
                            "CAR",
                            "TRUCK",
                            "CAR_GT",
                            "TUK_TUK",
                            "BICYCLE",
                            "PEDESTRIAN",
                            "PUBLIC_TRANSPORT"
                        ],
                        "nullable": false,
                        "type": "string"
                    }
                },
                "required": [
                    "key",
                    "transport_type"
                ],
                "type": "object"
            },
            "maxItems": 9000,
            "minItems": 1,
            "type": "array"
        },
        "points": {
            "items": {
                "additionalProperties": false,
                "nullable": true,
                "properties": {
                    "duration": {
                        "default": 10,
                        "format": "double",
                        "maximum": 43800,
                        "minimum": 0,
                        "type": "number"
                    },
                    "key": {
                        "maxLength": 1024,
                        "minLength": 1,
                        "type": "string"
                    },
                    "location": {
                        "additionalProperties": false,
                        "properties": {
                            "arrival_duration": {
                                "default": 0,
                                "format": "int32",
                                "maximum": 1440,
                                "minimum": 0,
                                "type": "integer"
                            },
                            "departure_duration": {
                                "default": 0,
                                "format": "int32",
                                "maximum": 1440,
                                "minimum": 0,
                                "type": "integer"
                            },
                            "latitude": {
                                "format": "double",
                                "maximum": 90,
                                "minimum": -90,
                                "type": "number"
                            },
                            "longitude": {
                                "format": "double",
                                "maximum": 180,
                                "minimum": -180,
                                "type": "number"
                            }
                        },
                        "required": [
                            "latitude",
                            "longitude"
                        ],
                        "type": "object"
                    }
                },
                "required": [
                    "key",
                    "location"
                ],
                "type": "object"
            },
            "maxItems": 9000,
            "minItems": 1,
            "type": "array"
        },
        "settings": {
            "additionalProperties": false,
            "properties": {
                "assumptions": {
                    "additionalProperties": false,
                    "nullable": false,
                    "properties": {
                        "flight_distance": {
                            "default": false,
                            "type": "boolean"
                        },
                        "traffic_jams": {
                            "default": true,
                            "type": "boolean"
                        }
                    },
                    "type": "object"
                },
                "calculation_time": {
                    "default": 40,
                    "format": "int32",
                    "maximum": 2880,
                    "minimum": 1,
                    "type": "integer"
                },
                "configuration": {
                    "default": "default",
                    "maxLength": 1000,
                    "minLength": 1,
                    "type": "string"
                },
                "limits": {
                    "additionalProperties": false,
                    "nullable": false,
                    "properties": {
                        "max_points": {
                            "default": 1,
                            "format": "int32",
                            "maximum": 7000,
                            "minimum": 1,
                            "type": "integer"
                        },
                        "min_points": {
                            "default": 1,
                            "format": "int32",
                            "maximum": 7000,
                            "minimum": 1,
                            "type": "integer"
                        }
                    },
                    "type": "object"
                },
                "precision": {
                    "default": 3,
                    "format": "int32",
                    "maximum": 6,
                    "minimum": 0,
                    "type": "integer"
                },
                "result_ttl": {
                    "default": 20,
                    "format": "int32",
                    "maximum": 14400,
                    "minimum": 1,
                    "type": "integer"
                },
                "routing": {
                    "default": [],
                    "items": {
                        "additionalProperties": false,
                        "properties": {
                            "matrix": {
                                "additionalProperties": false,
                                "nullable": true,
                                "properties": {
                                    "distances": {
                                        "items": {
                                            "items": {
                                                "format": "int64",
                                                "maximum": 10000000,
                                                "minimum": -1,
                                                "type": "integer"
                                            },
                                            "maxItems": 9000,
                                            "minItems": 2,
                                            "type": "array",
                                            "uniqueItems": false
                                        },
                                        "maxItems": 9000,
                                        "minItems": 2,
                                        "type": "array",
                                        "uniqueItems": false
                                    },
                                    "durations": {
                                        "items": {
                                            "items": {
                                                "format": "int64",
                                                "maximum": 10000000,
                                                "minimum": -1,
                                                "type": "integer"
                                            },
                                            "maxItems": 9000,
                                            "minItems": 2,
                                            "type": "array",
                                            "uniqueItems": false
                                        },
                                        "maxItems": 9000,
                                        "minItems": 2,
                                        "type": "array",
                                        "uniqueItems": false
                                    },
                                    "waypoints": {
                                        "items": {
                                            "additionalProperties": false,
                                            "nullable": true,
                                            "properties": {
                                                "duration": {
                                                    "default": 0,
                                                    "format": "int32",
                                                    "maximum": 43800,
                                                    "minimum": 0,
                                                    "type": "integer"
                                                },
                                                "latitude": {
                                                    "format": "double",
                                                    "maximum": 90,
                                                    "minimum": -90,
                                                    "type": "number"
                                                },
                                                "longitude": {
                                                    "format": "double",
                                                    "maximum": 180,
                                                    "minimum": -180,
                                                    "type": "number"
                                                },
                                                "name": {
                                                    "maxLength": 1024,
                                                    "minLength": 0,
                                                    "type": "string"
                                                }
                                            },
                                            "required": [
                                                "latitude",
                                                "longitude"
                                            ],
                                            "type": "object"
                                        },
                                        "maxItems": 9000,
                                        "minItems": 2,
                                        "type": "array",
                                        "uniqueItems": false
                                    }
                                },
                                "required": [
                                    "waypoints",
                                    "distances",
                                    "durations"
                                ],
                                "type": "object"
                            },
                            "traffic_jams": {
                                "items": {
                                    "additionalProperties": false,
                                    "properties": {
                                        "length_additive": {
                                            "default": 0,
                                            "format": "double",
                                            "maximum": 100000,
                                            "minimum": -100000,
                                            "type": "number"
                                        },
                                        "length_multiplier": {
                                            "default": 1,
                                            "format": "double",
                                            "maximum": 100,
                                            "minimum": 0,
                                            "type": "number"
                                        },
                                        "time_additive": {
                                            "default": 0,
                                            "format": "double",
                                            "maximum": 1440,
                                            "minimum": -1440,
                                            "type": "number"
                                        },
                                        "time_multiplier": {
                                            "default": 1,
                                            "format": "double",
                                            "maximum": 100,
                                            "minimum": 0,
                                            "type": "number"
                                        },
                                        "time_window": {
                                            "additionalProperties": false,
                                            "properties": {
                                                "from": {
                                                    "format": "date-time",
                                                    "type": "string"
                                                },
                                                "to": {
                                                    "format": "date-time",
                                                    "type": "string"
                                                }
                                            },
                                            "required": [
                                                "from",
                                                "to"
                                            ],
                                            "type": "object"
                                        }
                                    },
                                    "required": [
                                        "time_window"
                                    ],
                                    "type": "object"
                                },
                                "maxItems": 24,
                                "minItems": 0,
                                "type": "array"
                            },
                            "transport_type": {
                                "default": "CAR",
                                "enum": [
                                    "CAR",
                                    "TRUCK",
                                    "CAR_GT",
                                    "TUK_TUK",
                                    "BICYCLE",
                                    "PEDESTRIAN",
                                    "PUBLIC_TRANSPORT"
                                ],
                                "nullable": false,
                                "type": "string"
                            }
                        },
                        "required": [
                            "transport_type",
                            "matrix"
                        ],
                        "type": "object"
                    },
                    "maxItems": 7,
                    "minItems": 0,
                    "type": "array"
                },
                "transport_factor": {
                    "default": [],
                    "items": {
                        "additionalProperties": false,
                        "properties": {
                            "speed": {
                                "format": "double",
                                "maximum": 1000,
                                "minimum": 0.1,
                                "type": "number"
                            },
                            "transport_type": {
                                "default": "CAR",
                                "enum": [
                                    "CAR",
                                    "TRUCK",
                                    "CAR_GT",
                                    "TUK_TUK",
                                    "BICYCLE",
                                    "PEDESTRIAN",
                                    "PUBLIC_TRANSPORT"
                                ],
                                "nullable": false,
                                "type": "string"
                            }
                        },
                        "required": [
                            "transport_type",
                            "speed"
                        ],
                        "type": "object"
                    },
                    "maxItems": 7,
                    "minItems": 0,
                    "type": "array"
                }
            },
            "type": "object"
        }
    },
    "required": [
        "points",
        "performers"
    ],
    "type": "object"
}'''