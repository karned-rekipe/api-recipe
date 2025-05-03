import logging
from datetime import datetime, timezone

import httpx
from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from decorators.log_time import log_time_async
from services.inmemory_service import get_redis_api_db
from utils.path_util import is_unprotected_path
from config.config import URL_API_GATEWAY


r = get_redis_api_db()


def extract_licence(request: Request) -> str:
    return request.headers.get('licence')


def is_headers_licence_present(request: Request) -> bool:
    licence = extract_licence(request)
    if not licence:
        return False
    return True


def check_headers_licence(request: Request):
    if not is_headers_licence_present(request):
        raise HTTPException(status_code=403, detail="Licence header missing")


def is_licence_found(request: Request, licence: str):
    licenses = request.state.licenses
    if not licenses:
        return False
    if not any(licence_data['uuid'] == licence for licence_data in licenses):
        return False
    return True


def get_licences(token: str) -> list:
    response = httpx.get(f"{URL_API_GATEWAY}/licence/v1/mine", headers={"Authorization": f"Bearer {token}"})
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Licences request failed")
    return response.json()


def filter_licences(licences: list) -> list:
    now = int(datetime.now(timezone.utc).timestamp())
    licences_filtered = [
        {
            "uuid": lic["uuid"],
            "type_uuid": lic["type_uuid"],
            "name": lic["name"],
            "iat": lic["iat"],
            "exp": lic["exp"],
            "entity_uuid": lic["entity_uuid"]
        }
        for lic in licences if lic["iat"] < now < lic["exp"]
    ]
    return licences_filtered


def prepare_licences(token: str) -> list:
    licenses = get_licences(token)
    return filter_licences(licenses)


def refresh_licences(request: Request):
    token = request.state.token
    licenses = prepare_licences(token)
    request.state.licenses = licenses


def check_licence(request: Request, licence: str):
    if not is_licence_found(request, licence):
        refresh_licences(request)
        if not is_licence_found(request, licence):
            raise HTTPException(status_code=403, detail="Licence not found")


def extract_entity(request: Request):
    licenses = request.state.licenses
    license_uuid = request.state.licence_uuid
    for lic in licenses:
        if str(lic.get('uuid')) == str(license_uuid):
            return lic.get('entity_uuid')
    raise HTTPException(status_code=500, detail="Entity not found")


class LicenceVerificationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    @log_time_async
    async def dispatch(self, request: Request, call_next) -> Response:
        logging.info("LicenceVerificationMiddleware")
        try:
            if not is_unprotected_path(request.url.path):
                check_headers_licence(request)
                licence_uuid = extract_licence(request)
                logging.info(f"licence_uuid: {licence_uuid}")
                check_licence(request, licence_uuid)
                request.state.licence_uuid = licence_uuid
                entity_uuid = extract_entity(request)
                logging.info(f"entity_uuid: {entity_uuid}")
                request.state.entity_uuid = entity_uuid
            response = await call_next(request)
            return response
        except HTTPException as exc:
            return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
