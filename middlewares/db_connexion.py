import time

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import  Request
import logging

from config.config import ITEM_REPO


class DBConnectionMiddleware(BaseHTTPMiddleware):
    async def dispatch( self, request: Request, call_next ):
        start = time.time()
        logging.info("DBConnectionMiddleware: Start")

        repo = ITEM_REPO
        request.state.repo = repo

        print(request.state.token_info.get('user_id'))

        try:
            response = await call_next(request)
        finally:
            #request.state.repo.close() ne fonctionne pas !
            pass

        end = time.time()
        logging.info(f"DBConnectionMiddleware: Time elapsed: {end - start}")
        logging.info("DBConnectionMiddleware: End")
        return response