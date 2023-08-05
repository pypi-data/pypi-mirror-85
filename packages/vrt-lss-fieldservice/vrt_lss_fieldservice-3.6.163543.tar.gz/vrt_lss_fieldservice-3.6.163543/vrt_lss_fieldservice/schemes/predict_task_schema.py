PREDICT_TASK_SCHEMA = '''{
    "additionalProperties": false,
    "properties": {
        "id": {
            "format": "uuid",
            "type": "string"
        },
        "order": {
            "additionalProperties": false,
            "nullable": true,
            "properties": {
                "blacklist": {
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
                "duration": {
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
                },
                "restrictions": {
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
                "key",
                "location",
                "time_windows",
                "duration"
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