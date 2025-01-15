import time

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import  Request
import logging

from config.config import get_db
from decorators.log_time import log_time_async


class DBConnectionMiddleware(BaseHTTPMiddleware):
    @log_time_async
    async def dispatch( self, request: Request, call_next ):
        logging.info("DBConnectionMiddleware")
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