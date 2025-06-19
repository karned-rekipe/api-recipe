import httpx
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import HTTPException, Request
from services.logger_service import Logger

from starlette.responses import JSONResponse

from config.config import URL_API_GATEWAY
from shared.decorators.v0.log_time import log_time_async
from shared.middlewares.v0.token_middleware import extract_token
from repositories.recipe_repository import RecipeRepositoryMongo
from shared.services.v0.inmemory_service import get_redis_api_db
from shared.utils.v0.path_util import is_unprotected_path

r = get_redis_api_db()
logger = Logger()


def read_cache_credential(licence: str) -> dict | None:
    cache_key = f"{licence}_database"
    cached_result = r.get(cache_key)
    if cached_result is not None:
        logger.info(f"Using cached database credential for licence {licence}")
        return eval(cached_result)
    return None


def write_cache_credential(licence: str, credential: dict):
    cache_key = f"{licence}_database"
    r.set(cache_key, str(credential), ex=1800)
    logger.info(f"Cached database credential for licence {licence}")


def get_credential(token: str, licence: str) -> dict:
    cached_credential = read_cache_credential(licence)
    if cached_credential:
        return cached_credential

    response = httpx.get(url=f"{URL_API_GATEWAY}/credential/v1/database",
                         headers={"Authorization": f"Bearer {token}", "X-License-Key": f"{licence}"})
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Credential request failed")

    credential = response.json()
    write_cache_credential(licence, credential)

    return credential

def check_repo( repos ):
    if repos is None:
        raise Exception("DBConnectionMiddleware: Error: No repository found")


class DBConnectionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        logger.init("Initializing DBConnectionMiddleware")
        super().__init__(app)

    @log_time_async
    async def dispatch( self, request: Request, call_next ):
        try:
            if not is_unprotected_path(request.url.path):
                token = extract_token(request)
                credential = get_credential(token=token, licence=request.state.licence_uuid)

                repos = get_repositories(uri=credential.get('uri'))
                check_repo(repos)
                request.state.repos = repos

            response = await call_next(request)
            return response
        except HTTPException as exc:
            return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})