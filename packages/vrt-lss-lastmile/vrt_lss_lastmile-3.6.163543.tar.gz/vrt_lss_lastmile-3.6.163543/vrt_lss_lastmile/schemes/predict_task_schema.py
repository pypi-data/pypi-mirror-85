PREDICT_TASK_SCHEMA = '''{
    "additionalProperties": false,
    "properties": {
        "id": {
            "format": "uuid",
            "type": "string"
        },
        "locations": {
            "items": {
                "additionalProperties": false,
                "nullable": false,
                "properties": {
                    "comment": {
                        "maxLength": 10000,
                        "minLength": 0,
                        "type": "string"
                    },
                    "key": {
                        "maxLength": 1024,
                        "minLength": 1,
                        "type": "string"
                    },
                    "load_windows": {
                        "items": {
                            "additionalProperties": false,
                            "nullable": false,
                            "properties": {
                                "gates_count": {
                                    "default": 0,
                                    "format": "int32",
                                    "maximum": 9000,
                                    "minimum": 0,
                                    "type": "integer"
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
                            "type": "object"
                        },
                        "maxItems": 100,
                        "minItems": 0,
                        "type": "array"
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
                    },
                    "transport_restrictions": {
                        "items": {
                            "maxLength": 256,
                            "minLength": 1,
                            "type": "string"
                        },
                        "maxItems": 1000,
                        "minItems": 0,
                        "type": "array",
                        "uniqueItems": true
                    }
                },
                "required": [
                    "key",
                    "location"
                ],
                "type": "object"
            },
            "maxItems": 2,
            "minItems": 1,
            "type": "array"
        },
        "order": {
            "additionalProperties": false,
            "nullable": false,
            "properties": {
                "cargos": {
                    "items": {
                        "additionalProperties": false,
                        "nullable": true,
                        "properties": {
                            "capacity": {
                                "additionalProperties": false,
                                "nullable": true,
                                "properties": {
                                    "capacity_x": {
                                        "default": 0,
                                        "format": "double",
                                        "maximum": 1000000,
                                        "minimum": 0,
                                        "type": "number"
                                    },
                                    "capacity_y": {
                                        "default": 0,
                                        "format": "double",
                                        "maximum": 1000000,
                                        "minimum": 0,
                                        "type": "number"
                                    },
                                    "capacity_z": {
                                        "default": 0,
                                        "format": "double",
                                        "maximum": 1000000,
                                        "minimum": 0,
                                        "type": "number"
                                    },
                                    "mass": {
                                        "default": 0,
                                        "format": "double",
                                        "maximum": 1000000,
                                        "minimum": 0,
                                        "type": "number"
                                    },
                                    "volume": {
                                        "default": 0,
                                        "format": "double",
                                        "maximum": 1000000,
                                        "minimum": 0,
                                        "type": "number"
                                    }
                                },
                                "type": "object"
                            },
                            "height": {
                                "default": 0,
                                "format": "double",
                                "maximum": 1000000,
                                "minimum": 0,
                                "type": "number"
                            },
                            "key": {
                                "maxLength": 1024,
                                "minLength": 1,
                                "type": "string"
                            },
                            "length": {
                                "default": 0,
                                "format": "double",
                                "maximum": 1000000,
                                "minimum": 0,
                                "type": "number"
                            },
                            "max_storage_time": {
                                "default": 43800,
                                "format": "int32",
                                "maximum": 43800,
                                "minimum": 0,
                                "type": "integer"
                            },
                            "restrictions": {
                                "items": {
                                    "maxLength": 256,
                                    "minLength": 1,
                                    "type": "string"
                                },
                                "maxItems": 100,
                                "minItems": 0,
                                "type": "array",
                                "uniqueItems": true
                            },
                            "rotation": {
                                "default": [],
                                "items": {
                                    "default": "ALL",
                                    "enum": [
                                        "ALL",
                                        "YAW",
                                        "PITCH",
                                        "ROLL"
                                    ],
                                    "nullable": false,
                                    "type": "string"
                                },
                                "maxItems": 4,
                                "minItems": 0,
                                "type": "array",
                                "uniqueItems": true
                            },
                            "width": {
                                "default": 0,
                                "format": "double",
                                "maximum": 1000000,
                                "minimum": 0,
                                "type": "number"
                            }
                        },
                        "required": [
                            "key"
                        ],
                        "type": "object"
                    },
                    "maxItems": 1000,
                    "minItems": 0,
                    "type": "array"
                },
                "comment": {
                    "maxLength": 10000,
                    "minLength": 0,
                    "type": "string"
                },
                "demands": {
                    "items": {
                        "additionalProperties": false,
                        "nullable": false,
                        "properties": {
                            "comment": {
                                "maxLength": 10000,
                                "minLength": 0,
                                "type": "string"
                            },
                            "demand_type": {
                                "enum": [
                                    "PICKUP",
                                    "DROP",
                                    "WORK"
                                ],
                                "nullable": false,
                                "type": "string"
                            },
                            "key": {
                                "maxLength": 1024,
                                "minLength": 1,
                                "type": "string"
                            },
                            "possible_events": {
                                "items": {
                                    "additionalProperties": false,
                                    "nullable": false,
                                    "properties": {
                                        "duration": {
                                            "default": 0,
                                            "format": "int32",
                                            "maximum": 525600,
                                            "minimum": 0,
                                            "type": "integer"
                                        },
                                        "location_key": {
                                            "maxLength": 1024,
                                            "minLength": 1,
                                            "type": "string"
                                        },
                                        "reward": {
                                            "default": 1000,
                                            "format": "double",
                                            "maximum": 1000000,
                                            "minimum": 0,
                                            "type": "number"
                                        },
                                        "soft_time_window": {
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
                                        "location_key",
                                        "time_window"
                                    ],
                                    "type": "object"
                                },
                                "maxItems": 500,
                                "minItems": 1,
                                "type": "array"
                            },
                            "precedence_in_order": {
                                "default": 0,
                                "format": "int32",
                                "maximum": 9000,
                                "minimum": 0,
                                "type": "integer"
                            },
                            "precedence_in_trip": {
                                "default": 0,
                                "format": "int32",
                                "maximum": 9000,
                                "minimum": 0,
                                "type": "integer"
                            },
                            "target_cargos": {
                                "items": {
                                    "maxLength": 1024,
                                    "minLength": 1,
                                    "type": "string"
                                },
                                "maxItems": 1000,
                                "minItems": 0,
                                "type": "array",
                                "uniqueItems": true
                            }
                        },
                        "required": [
                            "key",
                            "demand_type",
                            "possible_events"
                        ],
                        "type": "object"
                    },
                    "maxItems": 1000,
                    "minItems": 1,
                    "type": "array"
                },
                "key": {
                    "maxLength": 1024,
                    "minLength": 1,
                    "type": "string"
                },
                "order_features": {
                    "items": {
                        "maxLength": 256,
                        "minLength": 1,
                        "type": "string"
                    },
                    "maxItems": 1000,
                    "minItems": 0,
                    "type": "array",
                    "uniqueItems": true
                },
                "order_restrictions": {
                    "items": {
                        "maxLength": 256,
                        "minLength": 1,
                        "type": "string"
                    },
                    "maxItems": 1000,
                    "minItems": 0,
                    "type": "array",
                    "uniqueItems": true
                },
                "performer_blacklist": {
                    "default": [],
                    "items": {
                        "maxLength": 256,
                        "minLength": 1,
                        "type": "string"
                    },
                    "maxItems": 1000,
                    "minItems": 0,
                    "type": "array",
                    "uniqueItems": true
                },
                "performer_restrictions": {
                    "default": [],
                    "items": {
                        "maxLength": 256,
                        "minLength": 1,
                        "type": "string"
                    },
                    "maxItems": 1000,
                    "minItems": 0,
                    "type": "array",
                    "uniqueItems": true
                }
            },
            "required": [
                "key",
                "demands"
            ],
            "type": "object"
        }
    },
    "required": [
        "id",
        "order",
        "locations"
    ],
    "type": "object"
}'''