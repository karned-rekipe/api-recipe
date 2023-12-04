# API config
api = 'recipe'
api_v = '5'

# Mongo DB config
mongo_instance_name = 'v1'
mongo_instance_code = 'z3x7gm9'
mongo_database = 'testDB'

# responses
responses_pattern = {
    "description": "",
    "content": {
        "application/json": {
            "schema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "example": ""
                    }
                }
            }
        }
    }
}

responses_messages = {
    200: 'Success',
    201: 'Created',
    202: 'Accepted',
    204: 'No content',
    400: 'Bad request',
    403: 'Not enough privileges',
    404: 'Not found',
    429: 'Too many requests',
    500: 'Internal server error',
}

responses = {
    status_code: {
        "description": description,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "example": description
                        }
                    }
                }
            }
        }
    }
    for status_code, description in responses_messages.items()
}

responses_default = {
    400: responses[400],
    403: responses[403],
    404: responses[404],
    429: responses[429],
    500: responses[500],
}

responses_update = responses_default.copy()
responses_update[204] = responses[204]

responses_delete = responses_default.copy()
responses_delete[202] = responses[202]

responses_healthcheck = responses_default.copy()
responses_healthcheck[200] = responses[200]
tmsg = 'API /v' + api_v + '/' + api + ' is LIVE!'
responses_healthcheck[200]['content']['application/json']['schema']['properties']['message']['example'] = tmsg

