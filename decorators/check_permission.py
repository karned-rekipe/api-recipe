import logging
from fastapi import status, Request, HTTPException
from functools import wraps
from typing import List

from config.config import API_NAME


def check_roles( list_roles: dict, permissions: List[str] ) -> None:
    required_permissions = []
    for perm in permissions:
        if "/" in perm:
            required_permissions.append(perm)
        else:
            required_permissions.append(f"{API_NAME}/{perm}")

    formatted_roles = []
    for api, roles_data in list_roles.items():
        if isinstance(roles_data, list):
            for role in roles_data:
                formatted_roles.append(f"{api}/{role}")
        elif isinstance(roles_data, dict) and 'roles' in roles_data:
            for role in roles_data['roles']:
                formatted_roles.append(f"{api}/{role}")
        else:
            formatted_roles.append(f"{api}/roles")

    if not any(perm in formatted_roles for perm in required_permissions):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions ! "
                   "Need : " + ", ".join(required_permissions) +
                   " / Got : " + ", ".join(formatted_roles)
        )


def check_permissions( permissions: List[str] ):
    def decorator( func ):
        @wraps(func)
        async def wrapper( request: Request, *args, **kwargs ):
            logging.info(f"Checking permissions {permissions}")
            logging.info(f"User: {request}")

            check_roles(request.state.token_info.get('user_roles'), permissions)

            return await func(request, *args, **kwargs)

        return wrapper

    return decorator
