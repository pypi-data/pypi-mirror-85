CLUSTER_RESULT_SCHEMA = '''{
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
            "type": "array"
        },
        "info": {
            "additionalProperties": false,
            "nullable": false,
            "properties": {
                "planning_time": {
                    "format": "int32",
                    "maximum": 2880,
                    "minimum": 0,
                    "type": "integer"
                },
                "result_version": {
                    "format": "int32",
                    "maximum": 1000000,
                    "minimum": 0,
                    "type": "integer"
                },
                "status": {
                    "enum": [
                        "WAITING",
                        "IN_PROGRESS",
                        "FINISHED_IN_TIME",
                        "FINISHED_OUT_OF_TIME",
                        "CANCELED",
                        "FAILED"
                    ],
                    "type": "string"
                },
                "waiting_time": {
                    "format": "int32",
                    "maximum": 2880,
                    "minimum": 0,
                    "type": "integer"
                }
            },
            "required": [
                "status"
            ],
            "type": "object"
        },
        "progress": {
            "format": "int32",
            "maximum": 100,
            "minimum": 0,
            "type": "integer"
        },
        "tracedata": {
            "additionalProperties": false,
            "properties": {
                "code": {
                    "maxLength": 256,
                    "minLength": 3,
                    "type": "string"
                }
            },
            "required": [
                "code"
            ],
            "type": "object"
        },
        "unclustered_points": {
            "items": {
                "additionalProperties": false,
                "properties": {
                    "point": {
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
                    "reason": {
                        "type": "string"
                    }
                },
                "required": [
                    "point"
                ],
                "type": "object"
            },
            "maxItems": 9000,
            "minItems": 0,
            "type": "array"
        },
        "validations": {
            "items": {
                "additionalProperties": false,
                "properties": {
                    "entity_key": {
                        "maxLength": 1024,
                        "type": "string"
                    },
                    "entity_type": {
                        "maxLength": 1024,
                        "type": "string"
                    },
                    "info": {
                        "type": "string"
                    },
                    "type": {
                        "enum": [
                            "info",
                            "warning",
                            "error"
                        ],
                        "nullable": false,
                        "type": "string"
                    }
                },
                "required": [
                    "type",
                    "info"
                ],
                "type": "object"
            },
            "maxItems": 9000,
            "minItems": 0,
            "type": "array"
        }
    },
    "type": "object"
}'''