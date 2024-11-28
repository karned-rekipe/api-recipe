import logging

from fastapi import status, Request, HTTPException
from functools import wraps
from typing import List

from config.config import API_NAME


def check_ressource(list_aud: dict) -> None:
    """
    Args:
        list_aud: A dictionary representing the audience claims from a token. This dictionary is checked to ensure it includes the required API name.

    Raises:
        HTTPException: If the required API name is not found in the credentials provided, an HTTP 403 Forbidden error is raised, indicating insufficient permissions.
    """
    if not API_NAME in list_aud:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions ! "
                   "Need : api-recipe / Got : " + ", ".join(list_aud)
        )

def check_roles(list_roles: list, permissions: List[str]) -> None:
    """
    Args:
        list_roles: A list of roles the current user possesses.
        permissions: A list of required permissions to access a resource.

    Raises:
        HTTPException: If the user lacks the necessary permissions, an HTTP 403 error is raised with a message detailing the required and provided roles.
    """
    if not any(perm in list_roles for perm in permissions):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions ! "
                   "Need : " + ", ".join(permissions) +
                   " / Got : " + ", ".join(list_roles)
        )

def check_permissions(permissions: List[str]):
    """
    Args:
        permissions: A list of string permissions required to access the wrapped function.

    The `check_permissions` function is a decorator that checks whether a given request has the necessary permissions to access a specific resource. The `permissions` parameter is a list of strings representing the permissions required. It wraps an asynchronous function and, when executed, logs the permissions and user information, verifies token information, and checks roles against the required permissions.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            logging.info(f"Checking permissions {permissions}")
            logging.info(f"User: {request}")

            check_ressource(request.state.token_info.get('resource_access'))
            check_roles(request.state.token_info.get('resource_access').get(API_NAME).get('roles'), permissions)

            return await func(request, *args, **kwargs)

        return wrapper

    return decorator