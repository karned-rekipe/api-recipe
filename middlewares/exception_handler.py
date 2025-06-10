from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from models.response_model import create_error_response

async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    error_code = f"HTTP_{exc.status_code}"
    error_message = str(exc.detail)
    error_response = create_error_response(error_code, error_message)

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response,
    )
