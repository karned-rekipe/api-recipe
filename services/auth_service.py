import os
from typing import Annotated

import httpx

from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
from config.config import KEYCLOAK_URL

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

    token_info = response.json()
    if not token_info.get("active"):
        raise HTTPException(status_code=401, detail="Invalid token")

    return token_info

def verif_token(token: Annotated[str, Depends(http_bearer)]):
    """
    Vérifie le token, d'abord via le cache JSON, sinon via Keycloak.
    """
    token = token.credentials

    token_info = introspect_token(token)

    return token_info