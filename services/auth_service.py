from typing import Annotated

import requests
import logging

from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer
from jose import jwt, JWTError, jwk
from config.config import API_NAME, KEYCLOAK_URL

http_bearer = HTTPBearer()

def get_config_openid():
    openid_config = requests.get(f"{KEYCLOAK_URL}/.well-known/openid-configuration").json()
    jwks_uri = openid_config["jwks_uri"]

    return jwks_uri


def get_jwks(jwks_uri):
    jwks = requests.get(jwks_uri).json()

    return jwks


def get_public_key(jwks):
    public_key = next((key for key in jwks["keys"] if key["alg"] == "RS256"), None)
    if not public_key:
        raise HTTPException(status_code=401, detail="Invalid token signing key")

    return public_key


def create_rsa_key(public_key):
    rsa_key = jwk.construct(public_key)

    return rsa_key


def decode_token(token, rsa_key):
    decoded_token = jwt.decode(token.credentials, rsa_key, algorithms=["RS256"], audience=API_NAME)
    logging.debug(f"Token décodé : {decoded_token}")

    return decoded_token


def verify_token(request: Request, token: Annotated[str, Depends(http_bearer)]):
    """Vérifier et décoder le token JWT"""
    try:
        jwks_uri = get_config_openid()
        logging.debug(f"Récupération des clés publiques depuis {jwks_uri}")

        jwks = get_jwks(jwks_uri)
        logging.debug(f"Clés JWKS récupérées : {jwks}")

        public_key = get_public_key(jwks)
        logging.debug(f"Clé publique trouvée : {public_key}")

        rsa_key = create_rsa_key(public_key)
        logging.debug(f"Clé publique construite : {rsa_key}")


        logging.debug(f"Token : {token}")
        logging.debug(f"Credentials : {token.credentials}")

        request.state.token_info = decode_token(token, rsa_key)
        return request.state.token_info
    except JWTError as e:
        logging.error(f"Erreur de décodage du token JWT : {str(e)}")
        raise HTTPException(status_code = 401, detail = "Invalid token")
    except Exception as e:
        logging.error(f"Erreur lors de la vérification du token : {str(e)}")
        raise HTTPException(status_code = 500, detail = "Internal server error")