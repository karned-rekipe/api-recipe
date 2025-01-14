import os
import time
from typing import Annotated
import httpx
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
from starlette.requests import Request

from config.config import API_NAME, KEYCLOAK_HOST, KEYCLOAK_REALM, get_redis_api_db

r = get_redis_api_db()
http_bearer = HTTPBearer()

def introspect_token(token: str) -> dict:
    url = f"{KEYCLOAK_HOST}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token/introspect"
    data = {
        "token": token,
        "client_id": os.environ.get("KEYCLOAK_CLIENT_ID"),
        "client_secret": os.environ.get("KEYCLOAK_CLIENT_SECRET")
    }

    response = httpx.post(url, data=data)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Keycloak introspection failed")
    return response.json()

def write_cache_token(token: str, token_info: dict):
    ttl = token_info.get("exp", int(time.time()) + 300) - int(time.time())
    r.set(token, str(token_info), ex=ttl)

def read_cache_token(token: str) -> dict:
    cached_result = r.get(token)
    if cached_result is not None:
        return eval(cached_result)

def get_token_info(token: str) -> dict:
    response = read_cache_token(token)
    if not response:
        response = introspect_token(token)
    write_cache_token(token, response)
    return response


def is_token_active(token_info: dict) -> bool:
    now = int(time.time())
    iat = token_info.get("iat")
    exp = token_info.get("exp")

    if iat is not None and exp is not None:
        expire_in = exp - now
        print(f"Token will expire in {expire_in} seconds")
        return iat < now < exp

    return False

def is_token_valid_audience(token_info: dict) -> bool:
    aud = token_info.get("aud")

    if API_NAME in aud:
        return True

    return False


def verif_token(request: Request, token: Annotated[str, Depends(http_bearer)]):
    token = token.credentials

    token_info = get_token_info(token)
    request.state.token_info = token_info

    if not is_token_active(token_info):
        raise HTTPException(status_code=401, detail="Token is not active")

    if not is_token_valid_audience(token_info):
        raise HTTPException(status_code=401, detail="Token is not valid for this audience")

