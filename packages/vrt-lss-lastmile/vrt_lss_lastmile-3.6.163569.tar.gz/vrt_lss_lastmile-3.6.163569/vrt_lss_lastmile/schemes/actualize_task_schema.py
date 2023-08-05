ACTUALIZE_TASK_SCHEMA = '''{
    "additionalProperties": false,
    "properties": {
        "actualize_settings": {
            "additionalProperties": false,
            "nullable": false,
            "properties": {
                "current_time": {
                    "format": "date-time",
                    "type": "string"
                },
                "ferry_crossing": {
                    "default": true,
                    "type": "boolean"
                },
                "geo_provider": {
                    "maxLength": 256,
                    "minLength": 1,
                    "type": "string"
                },
                "result_timezone": {
                    "default": 0,
                    "format": "int32",
                    "maximum": 12,
                    "minimum": -12,
                    "type": "integer"
                },
                "toll_roads": {
                    "default": true,
                    "type": "boolean"
                }
            },
            "type": "object"
        },
        "facts": {
            "additionalProperties": false,
            "properties": {
                "order_facts": {
                    "items": {
                        "additionalProperties": false,
                        "nullable": true,
                        "properties": {
                            "demand_facts": {
                                "items": {
                                    "additionalProperties": false,
                                    "nullable": true,
                                    "properties": {
                                        "demand_key": {
                                            "maxLength": 1024,
                                            "minLength": 1,
                                            "type": "string"
                                        },
                                        "job_facts": {
                                            "items": {
                                                "additionalProperties": false,
                                                "nullable": true,
                                                "properties": {
                                                    "job_type": {
                                                        "enum": [
                                                            "LOCATION_ARRIVAL",
                                                            "READY_TO_WORK",
                                                            "START_WORK",
                                                            "FINISH_WORK",
                                                            "LOCATION_DEPARTURE"
                                                        ],
                                                        "nullable": false,
                                                        "type": "string"
                                                    },
                                                    "time": {
                                                        "format": "date-time",
                                                        "type": "string"
                                                    }
                                                },
                                                "required": [
                                                    "time",
                                                    "job_type"
                                                ],
                                                "type": "object"
                                            },
                                            "type": "array"
                                        },
                                        "time": {
                                            "format": "date-time",
                                            "type": "string"
                                        },
                                        "type": {
                                            "enum": [
                                                "DONE",
                                                "CANCEL",
                                                "PROGRESS"
                                            ],
                                            "type": "string"
                                        }
                                    },
                                    "required": [
                                        "type",
                                        "time",
                                        "demand_key"
                                    ],
                                    "type": "object"
                                },
                                "type": "array"
                            },
                            "order_key": {
                                "maxLength": 1024,
                                "minLength": 1,
                                "type": "string"
                            },
                            "time": {
                                "format": "date-time",
                                "type": "string"
                            },
                            "type": {
                                "enum": [
                                    "DONE",
                                    "CANCEL",
                                    "PROGRESS"
                                ],
                                "type": "string"
                            }
                        },
                        "required": [
                            "type",
                            "time",
                            "order_key"
                        ],
                        "type": "object"
                    },
                    "type": "array"
                },
                "performer_facts": {
                    "items": {
                        "additionalProperties": false,
                        "nullable": true,
                        "properties": {
                            "performer_key": {
                                "maxLength": 1024,
                                "minLength": 1,
                                "type": "string"
                            },
                            "position": {
                                "additionalProperties": false,
                                "nullable": true,
                                "properties": {
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
                                    "time": {
                                        "format": "date-time",
                                        "type": "string"
                                    }
                                },
                                "required": [
                                    "latitude",
                                    "longitude",
                                    "time"
                                ],
                                "type": "object"
                            },
                            "time": {
                                "format": "date-time",
                                "type": "string"
                            }
                        },
                        "required": [
                            "time",
                            "performer_key",
                            "position"
                        ],
                        "type": "object"
                    },
                    "type": "array"
                },
                "transport_facts": {
                    "items": {
                        "additionalProperties": false,
                        "nullable": true,
                        "properties": {
                            "position": {
                                "additionalProperties": false,
                                "nullable": true,
                                "properties": {
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
                                    "time": {
                                        "format": "date-time",
                                        "type": "string"
                                    }
                                },
                                "required": [
                                    "latitude",
                                    "longitude",
                                    "time"
                                ],
                                "type": "object"
                            },
                            "time": {
                                "format": "date-time",
                                "type": "string"
                            },
                            "transport_key": {
                                "maxLength": 1024,
                                "minLength": 1,
                                "type": "string"
                            }
                        },
                        "required": [
                            "time",
                            "transport_key",
                            "position"
                        ],
                        "type": "object"
                    },
                    "type": "array"
                }
            },
            "type": "object"
        },
        "plan_result": {
            "additionalProperties": false,
            "properties": {
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
                "statistics": {
                    "additionalProperties": false,
                    "nullable": true,
                    "properties": {
                        "total_statistics": {
                            "additionalProperties": false,
                            "nullable": true,
                            "properties": {
                                "capacity_max": {
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
                                "capacity_utilization": {
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
                                "cost": {
                                    "format": "double",
                                    "minimum": 0,
                                    "type": "number"
                                },
                                "measurements": {
                                    "additionalProperties": false,
                                    "nullable": true,
                                    "properties": {
                                        "arriving_time": {
                                            "format": "int32",
                                            "minimum": 0,
                                            "type": "integer"
                                        },
                                        "departure_time": {
                                            "format": "int32",
                                            "minimum": 0,
                                            "type": "integer"
                                        },
                                        "distance": {
                                            "format": "int32",
                                            "minimum": 0,
                                            "type": "integer"
                                        },
                                        "driving_time": {
                                            "format": "int32",
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
                                        },
                                        "total_time": {
                                            "format": "int32",
                                            "minimum": 0,
                                            "type": "integer"
                                        },
                                        "waiting_time": {
                                            "format": "int32",
                                            "minimum": 0,
                                            "type": "integer"
                                        },
                                        "working_time": {
                                            "format": "int32",
                                            "minimum": 0,
                                            "type": "integer"
                                        }
                                    },
                                    "required": [
                                        "driving_time",
                                        "waiting_time",
                                        "working_time",
                                        "arriving_time",
                                        "departure_time",
                                        "total_time",
                                        "distance"
                                    ],
                                    "type": "object"
                                },
                                "orders_count": {
                                    "format": "int32",
                                    "maximum": 9000,
                                    "minimum": 0,
                                    "type": "integer"
                                },
                                "performers_count": {
                                    "format": "int32",
                                    "maximum": 9000,
                                    "minimum": 0,
                                    "type": "integer"
                                },
                                "plan_orders_count": {
                                    "format": "int32",
                                    "maximum": 9000,
                                    "minimum": 0,
                                    "type": "integer"
                                },
                                "quality": {
                                    "additionalProperties": false,
                                    "nullable": true,
                                    "properties": {
                                        "hard_time_window_violations": {
                                            "additionalProperties": false,
                                            "nullable": true,
                                            "properties": {
                                                "after": {
                                                    "additionalProperties": false,
                                                    "nullable": true,
                                                    "properties": {
                                                        "count": {
                                                            "format": "int32",
                                                            "maximum": 9000,
                                                            "minimum": 0,
                                                            "type": "integer"
                                                        },
                                                        "keys": {
                                                            "items": {
                                                                "maxLength": 1024,
                                                                "minLength": 1,
                                                                "type": "string"
                                                            },
                                                            "maxItems": 9000,
                                                            "minItems": 0,
                                                            "type": "array",
                                                            "uniqueItems": true
                                                        }
                                                    },
                                                    "type": "object"
                                                },
                                                "before": {
                                                    "additionalProperties": false,
                                                    "nullable": true,
                                                    "properties": {
                                                        "count": {
                                                            "format": "int32",
                                                            "maximum": 9000,
                                                            "minimum": 0,
                                                            "type": "integer"
                                                        },
                                                        "keys": {
                                                            "items": {
                                                                "maxLength": 1024,
                                                                "minLength": 1,
                                                                "type": "string"
                                                            },
                                                            "maxItems": 9000,
                                                            "minItems": 0,
                                                            "type": "array",
                                                            "uniqueItems": true
                                                        }
                                                    },
                                                    "type": "object"
                                                }
                                            },
                                            "type": "object"
                                        },
                                        "soft_time_window_violations": {
                                            "additionalProperties": false,
                                            "nullable": true,
                                            "properties": {
                                                "after": {
                                                    "additionalProperties": false,
                                                    "nullable": true,
                                                    "properties": {
                                                        "count": {
                                                            "format": "int32",
                                                            "maximum": 9000,
                                                            "minimum": 0,
                                                            "type": "integer"
                                                        },
                                                        "keys": {
                                                            "items": {
                                                                "maxLength": 1024,
                                                                "minLength": 1,
                                                                "type": "string"
                                                            },
                                                            "maxItems": 9000,
                                                            "minItems": 0,
                                                            "type": "array",
                                                            "uniqueItems": true
                                                        }
                                                    },
                                                    "type": "object"
                                                },
                                                "before": {
                                                    "additionalProperties": false,
                                                    "nullable": true,
                                                    "properties": {
                                                        "count": {
                                                            "format": "int32",
                                                            "maximum": 9000,
                                                            "minimum": 0,
                                                            "type": "integer"
                                                        },
                                                        "keys": {
                                                            "items": {
                                                                "maxLength": 1024,
                                                                "minLength": 1,
                                                                "type": "string"
                                                            },
                                                            "maxItems": 9000,
                                                            "minItems": 0,
                                                            "type": "array",
                                                            "uniqueItems": true
                                                        }
                                                    },
                                                    "type": "object"
                                                }
                                            },
                                            "type": "object"
                                        }
                                    },
                                    "required": [
                                        "soft_time_window_violations",
                                        "hard_time_window_violations"
                                    ],
                                    "type": "object"
                                },
                                "reward": {
                                    "format": "double",
                                    "minimum": 0,
                                    "type": "number"
                                },
                                "waitlist_orders_count": {
                                    "format": "int32",
                                    "maximum": 9000,
                                    "minimum": 0,
                                    "type": "integer"
                                }
                            },
                            "required": [
                                "cost",
                                "reward",
                                "measurements",
                                "orders_count",
                                "plan_orders_count",
                                "waitlist_orders_count",
                                "performers_count"
                            ],
                            "type": "object"
                        },
                        "trips_statistics": {
                            "items": {
                                "additionalProperties": false,
                                "nullable": true,
                                "properties": {
                                    "max_load": {
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
                                            "count": {
                                                "format": "int32",
                                                "minimum": 0,
                                                "type": "integer"
                                            }
                                        },
                                        "required": [
                                            "count",
                                            "capacity"
                                        ],
                                        "type": "object"
                                    },
                                    "statistics": {
                                        "additionalProperties": false,
                                        "nullable": true,
                                        "properties": {
                                            "capacity_max": {
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
                                            "capacity_utilization": {
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
                                            "cost": {
                                                "format": "double",
                                                "minimum": 0,
                                                "type": "number"
                                            },
                                            "measurements": {
                                                "additionalProperties": false,
                                                "nullable": true,
                                                "properties": {
                                                    "arriving_time": {
                                                        "format": "int32",
                                                        "minimum": 0,
                                                        "type": "integer"
                                                    },
                                                    "departure_time": {
                                                        "format": "int32",
                                                        "minimum": 0,
                                                        "type": "integer"
                                                    },
                                                    "distance": {
                                                        "format": "int32",
                                                        "minimum": 0,
                                                        "type": "integer"
                                                    },
                                                    "driving_time": {
                                                        "format": "int32",
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
                                                    },
                                                    "total_time": {
                                                        "format": "int32",
                                                        "minimum": 0,
                                                        "type": "integer"
                                                    },
                                                    "waiting_time": {
                                                        "format": "int32",
                                                        "minimum": 0,
                                                        "type": "integer"
                                                    },
                                                    "working_time": {
                                                        "format": "int32",
                                                        "minimum": 0,
                                                        "type": "integer"
                                                    }
                                                },
                                                "required": [
                                                    "driving_time",
                                                    "waiting_time",
                                                    "working_time",
                                                    "arriving_time",
                                                    "departure_time",
                                                    "total_time",
                                                    "distance"
                                                ],
                                                "type": "object"
                                            },
                                            "orders_count": {
                                                "format": "int32",
                                                "maximum": 9000,
                                                "minimum": 0,
                                                "type": "integer"
                                            },
                                            "performers_count": {
                                                "format": "int32",
                                                "maximum": 9000,
                                                "minimum": 0,
                                                "type": "integer"
                                            },
                                            "plan_orders_count": {
                                                "format": "int32",
                                                "maximum": 9000,
                                                "minimum": 0,
                                                "type": "integer"
                                            },
                                            "quality": {
                                                "additionalProperties": false,
                                                "nullable": true,
                                                "properties": {
                                                    "hard_time_window_violations": {
                                                        "additionalProperties": false,
                                                        "nullable": true,
                                                        "properties": {
                                                            "after": {
                                                                "additionalProperties": false,
                                                                "nullable": true,
                                                                "properties": {
                                                                    "count": {
                                                                        "format": "int32",
                                                                        "maximum": 9000,
                                                                        "minimum": 0,
                                                                        "type": "integer"
                                                                    },
                                                                    "keys": {
                                                                        "items": {
                                                                            "maxLength": 1024,
                                                                            "minLength": 1,
                                                                            "type": "string"
                                                                        },
                                                                        "maxItems": 9000,
                                                                        "minItems": 0,
                                                                        "type": "array",
                                                                        "uniqueItems": true
                                                                    }
                                                                },
                                                                "type": "object"
                                                            },
                                                            "before": {
                                                                "additionalProperties": false,
                                                                "nullable": true,
                                                                "properties": {
                                                                    "count": {
                                                                        "format": "int32",
                                                                        "maximum": 9000,
                                                                        "minimum": 0,
                                                                        "type": "integer"
                                                                    },
                                                                    "keys": {
                                                                        "items": {
                                                                            "maxLength": 1024,
                                                                            "minLength": 1,
                                                                            "type": "string"
                                                                        },
                                                                        "maxItems": 9000,
                                                                        "minItems": 0,
                                                                        "type": "array",
                                                                        "uniqueItems": true
                                                                    }
                                                                },
                                                                "type": "object"
                                                            }
                                                        },
                                                        "type": "object"
                                                    },
                                                    "soft_time_window_violations": {
                                                        "additionalProperties": false,
                                                        "nullable": true,
                                                        "properties": {
                                                            "after": {
                                                                "additionalProperties": false,
                                                                "nullable": true,
                                                                "properties": {
                                                                    "count": {
                                                                        "format": "int32",
                                                                        "maximum": 9000,
                                                                        "minimum": 0,
                                                                        "type": "integer"
                                                                    },
                                                                    "keys": {
                                                                        "items": {
                                                                            "maxLength": 1024,
                                                                            "minLength": 1,
                                                                            "type": "string"
                                                                        },
                                                                        "maxItems": 9000,
                                                                        "minItems": 0,
                                                                        "type": "array",
                                                                        "uniqueItems": true
                                                                    }
                                                                },
                                                                "type": "object"
                                                            },
                                                            "before": {
                                                                "additionalProperties": false,
                                                                "nullable": true,
                                                                "properties": {
                                                                    "count": {
                                                                        "format": "int32",
                                                                        "maximum": 9000,
                                                                        "minimum": 0,
                                                                        "type": "integer"
                                                                    },
                                                                    "keys": {
                                                                        "items": {
                                                                            "maxLength": 1024,
                                                                            "minLength": 1,
                                                                            "type": "string"
                                                                        },
                                                                        "maxItems": 9000,
                                                                        "minItems": 0,
                                                                        "type": "array",
                                                                        "uniqueItems": true
                                                                    }
                                                                },
                                                                "type": "object"
                                                            }
                                                        },
                                                        "type": "object"
                                                    }
                                                },
                                                "required": [
                                                    "soft_time_window_violations",
                                                    "hard_time_window_violations"
                                                ],
                                                "type": "object"
                                            },
                                            "reward": {
                                                "format": "double",
                                                "minimum": 0,
                                                "type": "number"
                                            },
                                            "waitlist_orders_count": {
                                                "format": "int32",
                                                "maximum": 9000,
                                                "minimum": 0,
                                                "type": "integer"
                                            }
                                        },
                                        "required": [
                                            "cost",
                                            "reward",
                                            "measurements",
                                            "orders_count",
                                            "plan_orders_count",
                                            "waitlist_orders_count",
                                            "performers_count"
                                        ],
                                        "type": "object"
                                    },
                                    "stop_statistics": {
                                        "items": {
                                            "additionalProperties": false,
                                            "nullable": true,
                                            "properties": {
                                                "current_load": {
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
                                                        "count": {
                                                            "format": "int32",
                                                            "minimum": 0,
                                                            "type": "integer"
                                                        }
                                                    },
                                                    "required": [
                                                        "count",
                                                        "capacity"
                                                    ],
                                                    "type": "object"
                                                },
                                                "demand_ids": {
                                                    "items": {
                                                        "maxLength": 1024,
                                                        "minLength": 1,
                                                        "type": "string"
                                                    },
                                                    "type": "array"
                                                },
                                                "download": {
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
                                                        "count": {
                                                            "format": "int32",
                                                            "minimum": 0,
                                                            "type": "integer"
                                                        }
                                                    },
                                                    "required": [
                                                        "count",
                                                        "capacity"
                                                    ],
                                                    "type": "object"
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
                                                "location_key": {
                                                    "maxLength": 1024,
                                                    "minLength": 1,
                                                    "type": "string"
                                                },
                                                "measurements": {
                                                    "additionalProperties": false,
                                                    "nullable": true,
                                                    "properties": {
                                                        "arriving_time": {
                                                            "format": "int32",
                                                            "minimum": 0,
                                                            "type": "integer"
                                                        },
                                                        "departure_time": {
                                                            "format": "int32",
                                                            "minimum": 0,
                                                            "type": "integer"
                                                        },
                                                        "distance": {
                                                            "format": "int32",
                                                            "minimum": 0,
                                                            "type": "integer"
                                                        },
                                                        "driving_time": {
                                                            "format": "int32",
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
                                                        },
                                                        "total_time": {
                                                            "format": "int32",
                                                            "minimum": 0,
                                                            "type": "integer"
                                                        },
                                                        "waiting_time": {
                                                            "format": "int32",
                                                            "minimum": 0,
                                                            "type": "integer"
                                                        },
                                                        "working_time": {
                                                            "format": "int32",
                                                            "minimum": 0,
                                                            "type": "integer"
                                                        }
                                                    },
                                                    "required": [
                                                        "driving_time",
                                                        "waiting_time",
                                                        "working_time",
                                                        "arriving_time",
                                                        "departure_time",
                                                        "total_time",
                                                        "distance"
                                                    ],
                                                    "type": "object"
                                                },
                                                "upload": {
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
                                                        "count": {
                                                            "format": "int32",
                                                            "minimum": 0,
                                                            "type": "integer"
                                                        }
                                                    },
                                                    "required": [
                                                        "count",
                                                        "capacity"
                                                    ],
                                                    "type": "object"
                                                }
                                            },
                                            "required": [
                                                "location",
                                                "measurements"
                                            ],
                                            "type": "object"
                                        },
                                        "maxItems": 9000,
                                        "minItems": 0,
                                        "type": "array"
                                    },
                                    "total_load": {
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
                                            "count": {
                                                "format": "int32",
                                                "minimum": 0,
                                                "type": "integer"
                                            }
                                        },
                                        "required": [
                                            "count",
                                            "capacity"
                                        ],
                                        "type": "object"
                                    },
                                    "trip_key": {
                                        "maxLength": 1024,
                                        "minLength": 1,
                                        "type": "string"
                                    }
                                },
                                "required": [
                                    "trip_key",
                                    "statistics",
                                    "stop_statistics"
                                ],
                                "type": "object"
                            },
                            "maxItems": 9000,
                            "minItems": 0,
                            "type": "array"
                        }
                    },
                    "required": [
                        "total_statistics",
                        "trips_statistics"
                    ],
                    "type": "object"
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
                "trips": {
                    "items": {
                        "additionalProperties": false,
                        "nullable": false,
                        "properties": {
                            "actions": {
                                "items": {
                                    "additionalProperties": false,
                                    "nullable": false,
                                    "properties": {
                                        "cargo_placements": {
                                            "items": {
                                                "additionalProperties": false,
                                                "properties": {
                                                    "box_key": {
                                                        "maxLength": 1024,
                                                        "minLength": 1,
                                                        "type": "string"
                                                    },
                                                    "cargo_key": {
                                                        "maxLength": 1024,
                                                        "minLength": 1,
                                                        "type": "string"
                                                    }
                                                },
                                                "required": [
                                                    "box_key",
                                                    "cargo_key"
                                                ],
                                                "type": "object"
                                            },
                                            "maxItems": 1000,
                                            "minItems": 0,
                                            "type": "array"
                                        },
                                        "demand_key": {
                                            "maxLength": 1024,
                                            "minLength": 1,
                                            "type": "string"
                                        },
                                        "location_key": {
                                            "maxLength": 1024,
                                            "minLength": 1,
                                            "type": "string"
                                        },
                                        "order_key": {
                                            "maxLength": 1024,
                                            "minLength": 1,
                                            "type": "string"
                                        },
                                        "todolist": {
                                            "items": {
                                                "additionalProperties": false,
                                                "nullable": false,
                                                "properties": {
                                                    "job_time": {
                                                        "format": "date-time",
                                                        "type": "string"
                                                    },
                                                    "job_type": {
                                                        "enum": [
                                                            "LOCATION_ARRIVAL",
                                                            "READY_TO_WORK",
                                                            "START_WORK",
                                                            "FINISH_WORK",
                                                            "LOCATION_DEPARTURE"
                                                        ],
                                                        "nullable": false,
                                                        "type": "string"
                                                    }
                                                },
                                                "required": [
                                                    "job_type",
                                                    "job_time"
                                                ],
                                                "type": "object"
                                            },
                                            "maxItems": 1000,
                                            "minItems": 1,
                                            "type": "array"
                                        }
                                    },
                                    "required": [
                                        "order_key",
                                        "demand_key",
                                        "location_key",
                                        "todolist"
                                    ],
                                    "type": "object"
                                },
                                "maxItems": 1000,
                                "minItems": 1,
                                "type": "array"
                            },
                            "assigned_shifts": {
                                "items": {
                                    "additionalProperties": false,
                                    "nullable": false,
                                    "properties": {
                                        "shift_key": {
                                            "maxLength": 1024,
                                            "minLength": 1,
                                            "type": "string"
                                        },
                                        "shift_time": {
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
                                        "shift_key",
                                        "shift_time"
                                    ],
                                    "type": "object"
                                },
                                "maxItems": 2,
                                "minItems": 2,
                                "type": "array"
                            },
                            "attributes": {
                                "default": [],
                                "items": {
                                    "maxLength": 10000,
                                    "minLength": 0,
                                    "type": "string"
                                },
                                "maxItems": 1000,
                                "minItems": 0,
                                "type": "array",
                                "uniqueItems": true
                            },
                            "finish_location_key": {
                                "maxLength": 1024,
                                "minLength": 1,
                                "type": "string"
                            },
                            "key": {
                                "maxLength": 1024,
                                "minLength": 1,
                                "type": "string"
                            },
                            "start_location_key": {
                                "maxLength": 1024,
                                "minLength": 1,
                                "type": "string"
                            },
                            "waitlist": {
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
                            "assigned_shifts"
                        ],
                        "type": "object"
                    },
                    "maxItems": 9000,
                    "minItems": 0,
                    "type": "array"
                },
                "unplanned_orders": {
                    "items": {
                        "additionalProperties": false,
                        "nullable": false,
                        "properties": {
                            "order": {
                                "additionalProperties": false,
                                "nullable": false,
                                "properties": {
                                    "attributes": {
                                        "default": [],
                                        "items": {
                                            "maxLength": 10000,
                                            "minLength": 0,
                                            "type": "string"
                                        },
                                        "maxItems": 1000,
                                        "minItems": 0,
                                        "type": "array",
                                        "uniqueItems": true
                                    },
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
                                    "demands": {
                                        "items": {
                                            "additionalProperties": false,
                                            "nullable": false,
                                            "properties": {
                                                "attributes": {
                                                    "default": [],
                                                    "items": {
                                                        "maxLength": 10000,
                                                        "minLength": 0,
                                                        "type": "string"
                                                    },
                                                    "maxItems": 1000,
                                                    "minItems": 0,
                                                    "type": "array",
                                                    "uniqueItems": true
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
                            },
                            "reason": {
                                "type": "string"
                            }
                        },
                        "required": [
                            "order"
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
            "required": [
                "trips"
            ],
            "type": "object"
        },
        "plan_task": {
            "additionalProperties": false,
            "properties": {
                "hardlinks": {
                    "items": {
                        "additionalProperties": false,
                        "nullable": false,
                        "properties": {
                            "key": {
                                "maxLength": 1024,
                                "minLength": 1,
                                "type": "string"
                            },
                            "links": {
                                "items": {
                                    "additionalProperties": false,
                                    "properties": {
                                        "entity_key": {
                                            "maxLength": 1024,
                                            "minLength": 1,
                                            "type": "string"
                                        },
                                        "type": {
                                            "enum": [
                                                "ORDER",
                                                "SHIFT"
                                            ],
                                            "nullable": false,
                                            "type": "string"
                                        }
                                    },
                                    "required": [
                                        "type",
                                        "entity_key"
                                    ],
                                    "type": "object"
                                },
                                "maxItems": 1000,
                                "minItems": 2,
                                "type": "array"
                            }
                        },
                        "required": [
                            "key",
                            "links"
                        ],
                        "type": "object"
                    },
                    "maxItems": 9000,
                    "minItems": 0,
                    "type": "array"
                },
                "locations": {
                    "items": {
                        "additionalProperties": false,
                        "nullable": false,
                        "properties": {
                            "attributes": {
                                "default": [],
                                "items": {
                                    "maxLength": 10000,
                                    "minLength": 0,
                                    "type": "string"
                                },
                                "maxItems": 1000,
                                "minItems": 0,
                                "type": "array",
                                "uniqueItems": true
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
                    "maxItems": 9000,
                    "minItems": 1,
                    "type": "array"
                },
                "orders": {
                    "items": {
                        "additionalProperties": false,
                        "nullable": false,
                        "properties": {
                            "attributes": {
                                "default": [],
                                "items": {
                                    "maxLength": 10000,
                                    "minLength": 0,
                                    "type": "string"
                                },
                                "maxItems": 1000,
                                "minItems": 0,
                                "type": "array",
                                "uniqueItems": true
                            },
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
                            "demands": {
                                "items": {
                                    "additionalProperties": false,
                                    "nullable": false,
                                    "properties": {
                                        "attributes": {
                                            "default": [],
                                            "items": {
                                                "maxLength": 10000,
                                                "minLength": 0,
                                                "type": "string"
                                            },
                                            "maxItems": 1000,
                                            "minItems": 0,
                                            "type": "array",
                                            "uniqueItems": true
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
                    },
                    "maxItems": 9000,
                    "minItems": 1,
                    "type": "array"
                },
                "performers": {
                    "items": {
                        "additionalProperties": false,
                        "nullable": false,
                        "properties": {
                            "attributes": {
                                "default": [],
                                "items": {
                                    "maxLength": 10000,
                                    "minLength": 0,
                                    "type": "string"
                                },
                                "maxItems": 1000,
                                "minItems": 0,
                                "type": "array",
                                "uniqueItems": true
                            },
                            "key": {
                                "maxLength": 1024,
                                "minLength": 1,
                                "type": "string"
                            },
                            "max_work_shifts": {
                                "default": 31,
                                "format": "int32",
                                "maximum": 31,
                                "minimum": 1,
                                "type": "integer"
                            },
                            "own_transport_type": {
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
                            },
                            "performer_features": {
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
                            "key"
                        ],
                        "type": "object"
                    },
                    "maxItems": 9000,
                    "minItems": 1,
                    "type": "array"
                },
                "settings": {
                    "additionalProperties": false,
                    "nullable": false,
                    "properties": {
                        "assumptions": {
                            "additionalProperties": false,
                            "nullable": false,
                            "properties": {
                                "disable_capacity": {
                                    "default": false,
                                    "type": "boolean"
                                },
                                "disable_compatibility": {
                                    "default": false,
                                    "type": "boolean"
                                },
                                "expand_shift_time_window": {
                                    "default": false,
                                    "type": "boolean"
                                },
                                "ferry_crossing": {
                                    "default": true,
                                    "type": "boolean"
                                },
                                "flight_distance": {
                                    "default": false,
                                    "type": "boolean"
                                },
                                "same_order_time_window": {
                                    "default": false,
                                    "type": "boolean"
                                },
                                "toll_roads": {
                                    "default": true,
                                    "type": "boolean"
                                },
                                "traffic_jams": {
                                    "default": true,
                                    "type": "boolean"
                                }
                            },
                            "type": "object"
                        },
                        "capacity_factor": {
                            "default": [],
                            "items": {
                                "additionalProperties": false,
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
                                    "capacity"
                                ],
                                "type": "object"
                            },
                            "maxItems": 7,
                            "minItems": 0,
                            "type": "array"
                        },
                        "configuration": {
                            "default": "default",
                            "maxLength": 1000,
                            "minLength": 1,
                            "type": "string"
                        },
                        "planning_time": {
                            "default": 20,
                            "format": "int32",
                            "maximum": 2880,
                            "minimum": 1,
                            "type": "integer"
                        },
                        "precision": {
                            "default": 2,
                            "format": "int32",
                            "maximum": 6,
                            "minimum": 0,
                            "type": "integer"
                        },
                        "predict_slots": {
                            "default": 0,
                            "format": "int32",
                            "maximum": 8,
                            "minimum": 0,
                            "type": "integer"
                        },
                        "result_timezone": {
                            "default": 0,
                            "format": "int32",
                            "maximum": 12,
                            "minimum": -12,
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
                },
                "shifts": {
                    "items": {
                        "additionalProperties": false,
                        "nullable": false,
                        "properties": {
                            "attributes": {
                                "default": [],
                                "items": {
                                    "maxLength": 10000,
                                    "minLength": 0,
                                    "type": "string"
                                },
                                "maxItems": 1000,
                                "minItems": 0,
                                "type": "array",
                                "uniqueItems": true
                            },
                            "availability_time": {
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
                            "finish_location_key": {
                                "maxLength": 1024,
                                "minLength": 1,
                                "type": "string"
                            },
                            "key": {
                                "maxLength": 1024,
                                "minLength": 1,
                                "type": "string"
                            },
                            "resource_key": {
                                "maxLength": 1024,
                                "minLength": 1,
                                "type": "string"
                            },
                            "shift_type": {
                                "enum": [
                                    "PERFORMER",
                                    "TRANSPORT"
                                ],
                                "nullable": false,
                                "type": "string"
                            },
                            "start_location_key": {
                                "maxLength": 1024,
                                "minLength": 1,
                                "type": "string"
                            },
                            "tariff": {
                                "additionalProperties": false,
                                "nullable": false,
                                "properties": {
                                    "constraints": {
                                        "items": {
                                            "additionalProperties": false,
                                            "nullable": false,
                                            "properties": {
                                                "cost_per_unit": {
                                                    "default": 0.001,
                                                    "format": "double",
                                                    "maximum": 10000,
                                                    "minimum": 0,
                                                    "type": "number"
                                                },
                                                "stage_length": {
                                                    "default": 100000000,
                                                    "format": "int32",
                                                    "maximum": 100000000,
                                                    "minimum": 1,
                                                    "type": "integer"
                                                }
                                            },
                                            "required": [
                                                "stage_length",
                                                "cost_per_unit"
                                            ],
                                            "type": "object"
                                        },
                                        "maxItems": 100,
                                        "minItems": 1,
                                        "type": "array"
                                    },
                                    "cost_per_shift": {
                                        "default": 0.001,
                                        "format": "double",
                                        "maximum": 100000,
                                        "minimum": 0,
                                        "type": "number"
                                    }
                                },
                                "required": [
                                    "cost_per_shift",
                                    "constraints"
                                ],
                                "type": "object"
                            },
                            "working_time": {
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
                            "key",
                            "shift_type",
                            "resource_key",
                            "availability_time",
                            "working_time"
                        ],
                        "type": "object"
                    },
                    "maxItems": 9000,
                    "minItems": 1,
                    "type": "array"
                },
                "transports": {
                    "items": {
                        "additionalProperties": false,
                        "nullable": false,
                        "properties": {
                            "attributes": {
                                "default": [],
                                "items": {
                                    "maxLength": 10000,
                                    "minLength": 0,
                                    "type": "string"
                                },
                                "maxItems": 1000,
                                "minItems": 0,
                                "type": "array",
                                "uniqueItems": true
                            },
                            "boxes": {
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
                                        "features": {
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
                                        "max_size": {
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
                                "maxItems": 100,
                                "minItems": 1,
                                "type": "array"
                            },
                            "key": {
                                "maxLength": 1024,
                                "minLength": 1,
                                "type": "string"
                            },
                            "performer_restrictions": {
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
                            "transport_features": {
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
                            "key"
                        ],
                        "type": "object"
                    },
                    "maxItems": 9000,
                    "minItems": 1,
                    "type": "array"
                },
                "trips": {
                    "items": {
                        "additionalProperties": false,
                        "nullable": false,
                        "properties": {
                            "actions": {
                                "items": {
                                    "additionalProperties": false,
                                    "nullable": false,
                                    "properties": {
                                        "cargo_placements": {
                                            "items": {
                                                "additionalProperties": false,
                                                "properties": {
                                                    "box_key": {
                                                        "maxLength": 1024,
                                                        "minLength": 1,
                                                        "type": "string"
                                                    },
                                                    "cargo_key": {
                                                        "maxLength": 1024,
                                                        "minLength": 1,
                                                        "type": "string"
                                                    }
                                                },
                                                "required": [
                                                    "box_key",
                                                    "cargo_key"
                                                ],
                                                "type": "object"
                                            },
                                            "maxItems": 1000,
                                            "minItems": 0,
                                            "type": "array"
                                        },
                                        "demand_key": {
                                            "maxLength": 1024,
                                            "minLength": 1,
                                            "type": "string"
                                        },
                                        "location_key": {
                                            "maxLength": 1024,
                                            "minLength": 1,
                                            "type": "string"
                                        },
                                        "order_key": {
                                            "maxLength": 1024,
                                            "minLength": 1,
                                            "type": "string"
                                        },
                                        "todolist": {
                                            "items": {
                                                "additionalProperties": false,
                                                "nullable": false,
                                                "properties": {
                                                    "job_time": {
                                                        "format": "date-time",
                                                        "type": "string"
                                                    },
                                                    "job_type": {
                                                        "enum": [
                                                            "LOCATION_ARRIVAL",
                                                            "READY_TO_WORK",
                                                            "START_WORK",
                                                            "FINISH_WORK",
                                                            "LOCATION_DEPARTURE"
                                                        ],
                                                        "nullable": false,
                                                        "type": "string"
                                                    }
                                                },
                                                "required": [
                                                    "job_type",
                                                    "job_time"
                                                ],
                                                "type": "object"
                                            },
                                            "maxItems": 1000,
                                            "minItems": 1,
                                            "type": "array"
                                        }
                                    },
                                    "required": [
                                        "order_key",
                                        "demand_key",
                                        "location_key",
                                        "todolist"
                                    ],
                                    "type": "object"
                                },
                                "maxItems": 1000,
                                "minItems": 1,
                                "type": "array"
                            },
                            "assigned_shifts": {
                                "items": {
                                    "additionalProperties": false,
                                    "nullable": false,
                                    "properties": {
                                        "shift_key": {
                                            "maxLength": 1024,
                                            "minLength": 1,
                                            "type": "string"
                                        },
                                        "shift_time": {
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
                                        "shift_key",
                                        "shift_time"
                                    ],
                                    "type": "object"
                                },
                                "maxItems": 2,
                                "minItems": 2,
                                "type": "array"
                            },
                            "attributes": {
                                "default": [],
                                "items": {
                                    "maxLength": 10000,
                                    "minLength": 0,
                                    "type": "string"
                                },
                                "maxItems": 1000,
                                "minItems": 0,
                                "type": "array",
                                "uniqueItems": true
                            },
                            "finish_location_key": {
                                "maxLength": 1024,
                                "minLength": 1,
                                "type": "string"
                            },
                            "key": {
                                "maxLength": 1024,
                                "minLength": 1,
                                "type": "string"
                            },
                            "start_location_key": {
                                "maxLength": 1024,
                                "minLength": 1,
                                "type": "string"
                            },
                            "waitlist": {
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
                            "assigned_shifts"
                        ],
                        "type": "object"
                    },
                    "maxItems": 9000,
                    "minItems": 0,
                    "type": "array"
                }
            },
            "required": [
                "locations",
                "orders",
                "performers",
                "transports",
                "shifts"
            ],
            "type": "object"
        }
    },
    "required": [
        "plan_task",
        "plan_result"
    ],
    "type": "object"
}'''