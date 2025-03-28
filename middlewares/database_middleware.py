import time

import httpx
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import HTTPException, Request
import logging

from starlette.responses import JSONResponse

from decorators.log_time import log_time_async
from middlewares.licence_middleware import get_licence_info
from middlewares.token_middleware import extract_token
from repositories.item_repository import ItemRepositoryMongo
from utils.path_util import is_unprotected_path


def extract_credentials(request: Request):
    licence_info = get_licence_info(request, request.state.licence)
    credential = licence_info.get('credential_uuid')
    return credential

def get_credential( token: str, credential_uuid: str) -> dict:
    # TODO: Replace with real URL
    url = "https://n8n.koden.bzh/webhook/5feaeeb0-a88d-4748-81e7-515e4388e3d4"
    logging.info(f"get_credential: {credential_uuid}")
    response = httpx.get(url, headers={"Authorization": f"Bearer {token}"})
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Licences request failed")

    return response.json()


def check_repo( repo ):
    if repo is None:
        raise Exception("DBConnectionMiddleware: Error: No repository found")


class DBConnectionMiddleware(BaseHTTPMiddleware):
    @log_time_async
    async def dispatch( self, request: Request, call_next ):
        logging.info("DBConnectionMiddleware")

        try:
            if not is_unprotected_path(request.url.path):
                token = extract_token(request)
                credential_uuid = extract_credentials(request)
                logging.info(f"credential_uuid: {credential_uuid}")
                credential = get_credential(token, credential_uuid)
                repo = ItemRepositoryMongo(uri=credential.get('uri'))
                check_repo(repo)
                request.state.repo = repo

            response = await call_next(request)
            return response
        except HTTPException as exc:
            return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})