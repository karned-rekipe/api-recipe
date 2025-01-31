import logging
import time

from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from decorators.log_time import log_time_async
from middlewares.token_middleware import extract_token, get_token_info, is_unprotected_path, refresh_cache_token


def extract_licence( request: Request ) -> str:
    return request.headers.get('licence')

def is_headers_licence_present( request: Request ) -> bool:
    licence = extract_licence(request)
    if not licence:
        return False
    return True

def is_licence_found( request: Request, licence: str ):
    token = extract_token(request)
    token_info = get_token_info(token)
    if not token_info.get('licenses'):
        return False
    licenses = token_info.get('licenses')
    if not licenses:
        return False
    if not any(licence_data['uuid'] == licence for licence_data in licenses):
        return False
    return True

def check_headers_licence( request: Request ):
    if not is_headers_licence_present(request):
        raise HTTPException(status_code=403, detail="Licence header missing")

def check_licence( request: Request, licence: str ):
    if not is_licence_found(request, licence):
        fresh_limit = int(time.time()) - 60
        if request.state.token_info.get('cached_time') < fresh_limit:
            refresh_cache_token(request)
            if not is_licence_found(request, licence):
                raise HTTPException(status_code=403, detail="Licence not found")

class LicenceVerificationMiddleware(BaseHTTPMiddleware):
    def __init__( self, app ):
        super().__init__(app)

    @log_time_async
    async def dispatch( self, request: Request, call_next ) -> Response:
        logging.info("LicenceVerificationMiddleware")

        if not is_unprotected_path(request.url.path):
            check_headers_licence(request)
            licence = extract_licence(request)
            check_licence(request, licence)
            request.state.licence = licence
        response = await call_next(request)
        return response