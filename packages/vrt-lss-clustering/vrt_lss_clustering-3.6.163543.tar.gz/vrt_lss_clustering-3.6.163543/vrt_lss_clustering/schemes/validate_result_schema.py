VALIDATE_RESULT_SCHEMA = '''{
    "additionalProperties": false,
    "properties": {
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
            "type": "array"
        }
    },
    "type": "object"
}'''