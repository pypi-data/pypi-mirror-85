STATISTICS_TASK_SCHEMA = '''{
    "additionalProperties": false,
    "properties": {
        "date_window": {
            "additionalProperties": false,
            "properties": {
                "from": {
                    "format": "date",
                    "type": "string"
                },
                "to": {
                    "format": "date",
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
}'''