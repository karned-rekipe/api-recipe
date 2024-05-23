import uvicorn
import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from icecream import ic

from recipe.config import *
from recipe.routers import recipe
from recipe.db import mongodb

ic.configureOutput(prefix = 'ic| -> ')

logging.basicConfig(level = logging.DEBUG)
logging.info('Start /' + api)


@asynccontextmanager
async def lifespan(app: FastAPI):
    mongodb.connect_to_database()
    yield
    mongodb.close_database_connection()


app = FastAPI(
    lifespan = lifespan,
    title = "/recipe",
    description = "API to manage recipes.",
    version = "1.0.1",
    openapi_url = '/' + api + '/openapi.json',
    docs_url = '/' + api + '/docs',
    redoc_url = None,
    terms_of_service = "https://api.koden.bzh/terms.html",
    contact = {
        "name": "Koden",
        "url": "https://www.koden.bzh",
        "email": "support@koden.bzh",
    },
    openapi_tags = [
        {
            'name': 'user',
            'description': "paths for users",
            "externalDocs": {
                "description": "External docs",
                "url": "https://www.koden.bzh",
            }
        },
        {
            'name': 'admin',
            'description': "paths for admins"
        }
    ])

# origins = ["http://127.0.0.1:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["GET", "POST", "PUT", "DELETE"],
    allow_headers = ["*"],
)

app.include_router(recipe.router, tags = ["user"], prefix = "/" + api)

if __name__ == "__main__" and os.environ.get("ENVIRONMENT") != "PRODUCTION":
    uvicorn.run(app, host = "127.0.0.1", port = 3000)
