PREDICT_TASK_SCHEMA = '''{
    "additionalProperties": false,
    "properties": {
        "id": {
            "format": "uuid",
            "type": "string"
        },
        "order": {
            "additionalProperties": false,
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
                    "minItems": 1,
                    "type": "array"
                },
                "cost": {
                    "additionalProperties": false,
                    "properties": {
                        "penalty": {
                            "additionalProperties": false,
                            "properties": {
                                "max_value": {
                                    "default": 0,
                                    "format": "double",
                                    "maximum": 1000000,
                                    "minimum": 0,
                                    "type": "number"
                                },
                                "period": {
                                    "default": 60,
                                    "format": "int32",
                                    "maximum": 1440,
                                    "minimum": 1,
                                    "type": "integer"
                                },
                                "start_time": {
                                    "format": "date-time",
                                    "type": "string"
                                },
                                "value": {
                                    "default": 0,
                                    "format": "double",
                                    "maximum": 1000000,
                                    "minimum": 0,
                                    "type": "number"
                                }
                            },
                            "required": [
                                "start_time",
                                "period",
                                "value",
                                "max_value"
                            ],
                            "type": "object"
                        },
                        "reward": {
                            "default": 1000,
                            "format": "double",
                            "maximum": 1000000,
                            "minimum": 0,
                            "type": "number"
                        }
                    },
                    "required": [
                        "reward"
                    ],
                    "type": "object"
                },
                "customer": {
                    "additionalProperties": false,
                    "properties": {
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
                        "time_windows": {
                            "items": {
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
                            "maxItems": 100,
                            "minItems": 1,
                            "type": "array"
                        }
                    },
                    "required": [
                        "location",
                        "time_windows"
                    ],
                    "type": "object"
                },
                "customer_duration": {
                    "default": 0,
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
                },
                "type": {
                    "default": "DROP",
                    "enum": [
                        "DROP",
                        "PICKUP"
                    ],
                    "nullable": false,
                    "type": "string"
                },
                "warehouse_duration": {
                    "default": 0,
                    "format": "double",
                    "maximum": 43800,
                    "minimum": 0,
                    "type": "number"
                },
                "warehouse_keys": {
                    "items": {
                        "maxLength": 1024,
                        "minLength": 1,
                        "type": "string"
                    },
                    "maxItems": 100,
                    "minItems": 1,
                    "type": "array"
                }
            },
            "required": [
                "key",
                "warehouse_keys",
                "customer",
                "cargos"
            ],
            "type": "object"
        }
    },
    "required": [
        "id",
        "order"
    ],
    "type": "object"
}'''