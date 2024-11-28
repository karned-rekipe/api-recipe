from fastapi import status, Request, HTTPException
from functools import wraps
from typing import List
import logging


def check_permissions(permissions: List[str]):
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            logging.info(f"Checking permissions {permissions}")
            logging.info(f"User: {request}")

            list_app = request.state.token_info.get('resource_access')

            if not 'api-recipe' in list_app:
                raise HTTPException(
                    status_code = status.HTTP_403_FORBIDDEN,
                    detail = "Insufficient permissions ! "
                             "Need : api-recipe / Got : " + ", ".join(list_app)
                )

            list_roles = list_app.get('api-recipe').get('roles')

            if not any(perm in list_roles for perm in permissions):
                raise HTTPException(
                    status_code = status.HTTP_403_FORBIDDEN,
                    detail = "Insufficient permissions ! "
                             "Need : " + ", ".join(permissions) +
                             " / Got : " + ", ".join(list_roles)
                )

            return await func(request, *args, **kwargs)

        return wrapper

    return decorator