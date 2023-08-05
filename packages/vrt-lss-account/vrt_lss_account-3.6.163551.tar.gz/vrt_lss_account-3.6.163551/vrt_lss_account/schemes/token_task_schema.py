TOKEN_TASK_SCHEMA = '''{
    "additionalProperties": false,
    "properties": {
        "password": {
            "maxLength": 1000,
            "minLength": 1,
            "type": "string"
        },
        "ttl_seconds": {
            "default": 86400,
            "format": "int32",
            "maximum": 31556926,
            "minimum": 60,
            "type": "integer"
        },
        "username": {
            "maxLength": 256,
            "minLength": 1,
            "type": "string"
        }
    },
    "required": [
        "username",
        "password"
    ],
    "type": "object"
}'''