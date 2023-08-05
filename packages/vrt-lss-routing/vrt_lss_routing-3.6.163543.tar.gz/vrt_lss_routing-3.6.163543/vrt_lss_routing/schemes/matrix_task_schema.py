MATRIX_TASK_SCHEMA = '''{
    "additionalProperties": false,
    "properties": {
        "departure_time": {
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
        "toll_roads": {
            "default": true,
            "type": "boolean"
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
        "waypoints"
    ],
    "type": "object"
}'''