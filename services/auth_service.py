from typing import Annotated

import requests
import logging

from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
from jose import jwt, JWTError, jwk
from config.config import CLIENT_ID

# Nouvelle configuration de sécurité pour Bearer Token dans Swagger
http_bearer = HTTPBearer()

# token: str = Depends(http_bearer)
def verify_token(token: Annotated[str, Depends(http_bearer)]):
    """Vérifier et décoder le token JWT"""
    try:
        # Récupérer la configuration OpenID de Keycloak
        openid_config = requests.get(f"https://iam.karned.bzh/realms/Karned/.well-known/openid-configuration").json()
        jwks_uri = openid_config["jwks_uri"]
        logging.debug(f"Récupération des clés publiques depuis {jwks_uri}")

        # Récupérer les clés JWKS
        jwks = requests.get(jwks_uri).json()
        logging.debug(f"Clés JWKS récupérées : {jwks}")

        # Trouver la clé publique qui correspond au JWT
        key = next((key for key in jwks["keys"] if key["alg"] == "RS256"), None)
        if not key:
            raise HTTPException(status_code = 401, detail = "Invalid token signing key")

        logging.debug(f"Clé publique trouvée : {key}")

        # Construire la clé publique RSA
        public_key = jwk.construct(key)  # Utilisation de jwk.construct() pour créer la clé RSA
        logging.debug(f"Clé publique construite : {public_key}")
        logging.debug(f"Token : {token}")
        logging.debug(f"Credentials : {token.credentials}")

        decoded_token = jwt.decode(token.credentials, public_key, algorithms = ["RS256"], audience = CLIENT_ID)
        logging.debug(f"Token décodé : {decoded_token}")
        logging.debug(f"Audience du token : {decoded_token.get('aud')}")

        return decoded_token
    except JWTError as e:
        logging.error(f"Erreur de décodage du token JWT : {str(e)}")
        raise HTTPException(status_code = 401, detail = "Invalid token")
    except Exception as e:
        logging.error(f"Erreur lors de la vérification du token : {str(e)}")
        raise HTTPException(status_code = 500, detail = "Internal server error")