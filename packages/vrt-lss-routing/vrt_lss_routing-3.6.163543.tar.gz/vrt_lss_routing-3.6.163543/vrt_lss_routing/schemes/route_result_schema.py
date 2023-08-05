ROUTE_RESULT_SCHEMA = '''{
    "additionalProperties": false,
    "properties": {
        "route": {
            "additionalProperties": false,
            "properties": {
                "legs": {
                    "items": {
                        "additionalProperties": false,
                        "properties": {
                            "statistics": {
                                "additionalProperties": false,
                                "nullable": true,
                                "properties": {
                                    "distance": {
                                        "format": "int32",
                                        "minimum": 0,
                                        "type": "integer"
                                    },
                                    "duration": {
                                        "format": "int32",
                                        "minimum": 0,
                                        "type": "integer"
                                    },
                                    "stopping_time": {
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
                                    }
                                },
                                "required": [
                                    "distance",
                                    "duration"
                                ],
                                "type": "object"
                            },
                            "steps": {
                                "items": {
                                    "additionalProperties": false,
                                    "properties": {
                                        "polyline": {
                                            "additionalProperties": false,
                                            "properties": {
                                                "points": {
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
                                                    "type": "array"
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
                                    "type": "object"
                                },
                                "type": "array"
                            }
                        },
                        "type": "object"
                    },
                    "type": "array"
                },
                "statistics": {
                    "additionalProperties": false,
                    "nullable": true,
                    "properties": {
                        "distance": {
                            "format": "int32",
                            "minimum": 0,
                            "type": "integer"
                        },
                        "duration": {
                            "format": "int32",
                            "minimum": 0,
                            "type": "integer"
                        },
                        "stopping_time": {
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
                        }
                    },
                    "required": [
                        "distance",
                        "duration"
                    ],
                    "type": "object"
                }
            },
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
        }
    },
    "required": [
        "route"
    ],
    "type": "object"
}'''