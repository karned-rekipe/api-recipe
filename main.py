from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBearer

from shared.config import init_config
from config.config import API_NAME, URL_API_GATEWAY, KEYCLOAK_HOST, KEYCLOAK_REALM, KEYCLOAK_CLIENT_ID, \
    KEYCLOAK_CLIENT_SECRET, UNLICENSED_PATHS, UNPROTECTED_PATHS, REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD
from shared.middlewares.v0.exception_handler import http_exception_handler
from shared.middlewares.v0.token_middleware import TokenVerificationMiddleware
from middlewares.database_middleware import DBConnectionMiddleware
from shared.middlewares.v0.licence_middleware import LicenceVerificationMiddleware
from shared.middlewares.v0.cors_middleware import CORSMiddleware
from routers import v1
import logging

logging.basicConfig(level=logging.INFO)
logging.info("Starting API")

logging.info("Loading Config for shared")
init_config(
    api_name=API_NAME,
    url_api_gateway=URL_API_GATEWAY,
    keycloak_host=KEYCLOAK_HOST,
    keycloak_realm=KEYCLOAK_REALM,
    keycloak_client_id=KEYCLOAK_CLIENT_ID,
    keycloak_client_secret=KEYCLOAK_CLIENT_SECRET,
    unlicensed_path=UNLICENSED_PATHS,
    unprotected_path=UNPROTECTED_PATHS,
    redis_host=REDIS_HOST,
    redis_db=REDIS_DB,
    redis_port=REDIS_PORT,
    redis_password=REDIS_PASSWORD
)
logging.info("End loading Config for shared")

bearer_scheme = HTTPBearer()

app = FastAPI(openapi_url="/recipe/openapi.json")
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="API Recipe",
        version="1.0.0",
        description="Cookbook recipe for all !",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        },
        "LicenceHeader": {
            "type": "apiKey",
            "in": "header",
            "name": "X-License-Key"
        }
    }
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [
                {"BearerAuth": []},
                {"LicenceHeader": []}
            ]
    app.openapi_schema = openapi_schema
    return app.openapi_schema
app.openapi = custom_openapi

app.add_middleware(DBConnectionMiddleware)
app.add_middleware(LicenceVerificationMiddleware)
app.add_middleware(TokenVerificationMiddleware)
app.add_middleware(CORSMiddleware)

app.add_exception_handler(HTTPException, http_exception_handler)

app.include_router(v1.router)
