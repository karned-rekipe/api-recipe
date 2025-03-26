import os

API_NAME = os.environ['API_NAME']
API_TAG_NAME = os.environ['API_TAG_NAME']

KEYCLOAK_HOST = os.environ['KEYCLOAK_HOST']
KEYCLOAK_REALM = os.environ['KEYCLOAK_REALM']
KEYCLOAK_CLIENT_ID = os.environ['KEYCLOAK_CLIENT_ID']
KEYCLOAK_CLIENT_SECRET = os.environ['KEYCLOAK_CLIENT_SECRET']

REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = int(os.environ['REDIS_PORT'])
REDIS_DB = int(os.environ['REDIS_DB'])
REDIS_PASSWORD = os.environ['REDIS_PASSWORD']

UNPROTECTED_PATHS = ['/favicon.ico', '/docs', '/openapi.json']

URL_API_GATEWAY = os.environ['URL_API_GATEWAY']