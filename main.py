from fastapi import FastAPI

from middlewares.auth_service import TokenVerificationMiddleware
from middlewares.db_connexion import DBConnectionMiddleware
from routers import items_router
import logging

logging.basicConfig(level=logging.INFO)
logging.info("Starting API")

app = FastAPI()
app.add_middleware(DBConnectionMiddleware)
app.add_middleware(TokenVerificationMiddleware)

app.include_router(items_router.router)