STATISTICS_RESULT_SCHEMA = '''{
    "additionalProperties": false,
    "properties": {
        "dates": {
            "items": {
                "additionalProperties": false,
                "properties": {
                    "date": {
                        "format": "date",
                        "type": "string"
                    },
                    "services": {
                        "items": {
                            "additionalProperties": false,
                            "properties": {
                                "methods": {
                                    "items": {
                                        "additionalProperties": false,
                                        "properties": {
                                            "method": {
                                                "enum": [
                                                    "plan",
                                                    "convert",
                                                    "analytics",
                                                    "predict",
                                                    "actualize",
                                                    "validate",
                                                    "route",
                                                    "matrix",
                                                    "cluster"
                                                ],
                                                "type": "string"
                                            },
                                            "points_per_day": {
                                                "default": 0,
                                                "format": "int32",
                                                "maximum": 10000000,
                                                "minimum": 0,
                                                "type": "integer"
                                            },
                                            "unique_points_per_day": {
                                                "default": 0,
                                                "format": "int32",
                                                "maximum": 10000000,
                                                "minimum": 0,
                                                "type": "integer"
                                            }
                                        },
                                        "required": [
                                            "method",
                                            "unique_points_per_day",
                                            "points_per_day"
                                        ],
                                        "type": "object"
                                    },
                                    "minItems": 1,
                                    "type": "array"
                                },
                                "service": {
                                    "enum": [
                                        "Lastmile",
                                        "Delivery",
                                        "FieldService",
                                        "Merchandiser",
                                        "Routing",
                                        "Clustering",
                                        "Account",
                                        "Partner"
                                    ],
                                    "type": "string"
                                }
                            },
                            "required": [
                                "service",
                                "methods"
                            ],
                            "type": "object"
                        },
                        "minItems": 1,
                        "type": "array"
                    }
                },
                "required": [
                    "date",
                    "services"
                ],
                "type": "object"
            },
            "minItems": 1,
            "type": "array"
        },
        "username": {
            "maxLength": 256,
            "minLength": 2,
            "type": "string"
        }
    },
    "required": [
        "username",
        "dates"
    ],
    "type": "object"
}'''