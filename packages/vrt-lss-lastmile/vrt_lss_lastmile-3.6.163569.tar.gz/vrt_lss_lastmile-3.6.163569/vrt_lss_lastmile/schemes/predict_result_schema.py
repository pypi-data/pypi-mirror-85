PREDICT_RESULT_SCHEMA = '''{
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
        "windows": {
            "items": {
                "additionalProperties": false,
                "properties": {
                    "cost": {
                        "format": "double",
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
                    "time_window",
                    "cost"
                ],
                "type": "object"
            },
            "type": "array"
        }
    },
    "type": "object"
}'''