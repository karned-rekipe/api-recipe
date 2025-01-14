import os
import time
from typing import Annotated

import httpx

from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
from config.config import API_NAME, KEYCLOAK_URL

http_bearer = HTTPBearer()

def introspect_token(token: str):
    url = f"{KEYCLOAK_URL}/token/introspect"
    data = {
        "token": token,
        "client_id": os.environ.get("CLIENT_ID"),
        "client_secret": os.environ.get("CLIENT_SECRET")
    }

    response = httpx.post(url, data=data)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Keycloak introspection failed")

    return response.json()

def is_token_active(token_info: dict):
    result = False
    iat = token_info.get("iat")
    exp = token_info.get("exp")
    now = int(time.time())
    print(f"iat: {iat}", f"exp: {exp}", f"now: {now}")
    if iat < now < exp:
        result = True

    return result

def is_token_valid_audience(token_info: dict):
    result = False
    aud = token_info.get("aud")
    print(f"aud: {aud}", f"API_NAME: {API_NAME}")
    if API_NAME in aud:
        result = True

    return result


def verif_token(token: Annotated[str, Depends(http_bearer)]):
    token = token.credentials

    token_info = introspect_token(token)

    if not is_token_active(token_info):
        raise HTTPException(status_code=401, detail="Token is not active")

    if not is_token_valid_audience(token_info):
        raise HTTPException(status_code=401, detail="Token is not valid for this audience")