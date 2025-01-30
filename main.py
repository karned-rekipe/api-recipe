from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBearer
from starlette.middleware import Middleware

from middlewares.token_middleware import TokenVerificationMiddleware
from middlewares.database_middleware import DBConnectionMiddleware
from middlewares.licence_middleware import LicenceVerificationMiddleware
from routers import items_router
import logging

logging.basicConfig(level=logging.INFO)
logging.info("Starting API")

bearer_scheme = HTTPBearer()

app = FastAPI()
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
            "name": "licence"
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

app.include_router(items_router.router)