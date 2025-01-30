import logging
from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from decorators.log_time import log_time_async


class LicenceVerificationMiddleware(BaseHTTPMiddleware):
    def __init__( self, app ):
        super().__init__(app)

    @log_time_async
    async def dispatch( self, request: Request, call_next ) -> Response:
        logging.info("LicenceVerificationMiddleware")

        unprotected_paths = ['/favicon.ico', '/docs', '/openapi.json']

        if request.url.path.lower() not in unprotected_paths:
            licence = request.headers.get('licence')
            if not licence:
                raise HTTPException(status_code=403, detail="Licence header missing")
            request.state.licence = licence
        response = await call_next(request)
        return response