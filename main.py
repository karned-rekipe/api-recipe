from fastapi import FastAPI, Path
from starlette import status
from routers import items

app = FastAPI()
app.include_router(items.router)
