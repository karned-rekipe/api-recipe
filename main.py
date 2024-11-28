from fastapi import FastAPI
from routers import items_router
import logging

# Configurez le logger pour afficher les informations dans la console
# logging.basicConfig(level = logging.DEBUG)

app = FastAPI()

app.include_router(items_router.router)