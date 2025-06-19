from typing import List

from fastapi import HTTPException, status

from config.config import API_NAME
from services.role_service import get_api_roles, get_app_roles


def format_required_permissions(permissions: List[str]) -> List[str]:
    required_permissions = []
    for perm in permissions:
        if "/" in perm:
            required_permissions.append(perm)
        else:
            required_permissions.append(f"{API_NAME}/{perm}")
    return required_permissions


def format_user_roles(api_roles: dict, app_roles: dict) -> List[str]:
    formatted_roles = []

    if api_roles:
        for api, roles_dict in api_roles.items():
            roles_list = roles_dict.get('roles', [])
            for role in roles_list:
                formatted_roles.append(f"{api}/{role}")

    if app_roles:
        for app, roles_dict in app_roles.items():
            roles_list = roles_dict.get('roles', [])
            for role in roles_list:
                formatted_roles.append(f"{app}/{role}")
                
    return formatted_roles


def check_user_has_permissions(request, permissions: List[str]) -> None:
    required_permissions = format_required_permissions(permissions)

    api_roles = get_api_roles(request)
    app_roles = get_app_roles(request)
    formatted_roles = format_user_roles(api_roles, app_roles)

    if not any(perm in formatted_roles for perm in required_permissions):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions ! "
                   "Need : " + ", ".join(required_permissions) +
                   " / Got : " + ", ".join(formatted_roles)
        )