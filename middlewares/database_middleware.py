import time

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import  Request
import logging

from decorators.log_time import log_time_async
from services.db_service import get_db


class DBConnectionMiddleware(BaseHTTPMiddleware):
    @log_time_async
    async def dispatch( self, request: Request, call_next ):
        logging.info("DBConnectionMiddleware")
        without_db_paths = ['/favicon.ico', '/docs', '/openapi.json']
        logging.info(request.url.path)

        if request.url.path.lower() not in without_db_paths:
            try:
                repo = get_db(request.state.token_info.get('user_id'))

                if repo is None:
                    raise Exception("DBConnectionMiddleware: Error: No repository found")

                request.state.repo = repo
            except Exception as e:
                logging.error(f"DBConnectionMiddleware: Error: {e}")
                raise e

        try:
            response = await call_next(request)
        finally:
            #request.state.repo.close() ne fonctionne pas !
            pass

        return response