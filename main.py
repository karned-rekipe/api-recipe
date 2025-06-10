from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBearer

from middlewares.exception_handler import http_exception_handler
from middlewares.token_middleware import TokenVerificationMiddleware
from middlewares.database_middleware import DBConnectionMiddleware
from middlewares.licence_middleware import LicenceVerificationMiddleware
from middlewares.cors_middleware import CORSMiddleware
from routers import v1
import logging

logging.basicConfig(level=logging.INFO)
logging.info("Starting API")

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
app.add_middleware(HTTPException, http_exception_handler)
app.add_middleware(LicenceVerificationMiddleware)
app.add_middleware(TokenVerificationMiddleware)
app.add_middleware(CORSMiddleware)

app.include_router(v1.router)
