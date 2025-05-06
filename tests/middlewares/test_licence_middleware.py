import pytest
import time
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi import HTTPException, Request
from starlette.responses import JSONResponse
from datetime import datetime, timezone

from middlewares.licence_middleware import (
    extract_licence, is_headers_licence_present, check_headers_licence,
    is_licence_found, get_licences, filter_licences, prepare_licences,
    refresh_cache_token, refresh_licences, check_licence, extract_entity,
    LicenceVerificationMiddleware
)


def test_extract_licence():
    mock_request = MagicMock(spec=Request)
    mock_request.headers = {"X-License-Key": "test-licence"}
    
    licence = extract_licence(mock_request)
    
    assert licence == "test-licence"


def test_extract_licence_missing():
    mock_request = MagicMock(spec=Request)
    mock_request.headers = {}
    
    licence = extract_licence(mock_request)
    
    assert licence is None


def test_is_headers_licence_present_valid():
    mock_request = MagicMock(spec=Request)
    mock_request.headers = {"X-License-Key": "test-licence"}
    
    with patch('middlewares.licence_middleware.extract_licence', return_value="test-licence"):
        assert is_headers_licence_present(mock_request)


def test_is_headers_licence_present_missing():
    mock_request = MagicMock(spec=Request)
    mock_request.headers = {}
    
    with patch('middlewares.licence_middleware.extract_licence', return_value=None):
        assert not is_headers_licence_present(mock_request)


def test_check_headers_licence_valid():
    mock_request = MagicMock(spec=Request)
    mock_request.headers = {"X-License-Key": "test-licence"}
    
    with patch('middlewares.licence_middleware.is_headers_licence_present', return_value=True):
        # Should not raise an exception
        check_headers_licence(mock_request)


def test_check_headers_licence_missing():
    mock_request = MagicMock(spec=Request)
    mock_request.headers = {}
    
    with patch('middlewares.licence_middleware.is_headers_licence_present', return_value=False):
        with pytest.raises(HTTPException) as exc:
            check_headers_licence(mock_request)
        
        assert exc.value.status_code == 403
        assert exc.value.detail == "Licence header missing"


def test_is_licence_found_valid():
    mock_request = MagicMock(spec=Request)
    mock_request.state.licenses = [
        {"uuid": "test-licence-1", "name": "Test Licence 1"},
        {"uuid": "test-licence-2", "name": "Test Licence 2"}
    ]
    
    assert is_licence_found(mock_request, "test-licence-1")


def test_is_licence_found_invalid():
    mock_request = MagicMock(spec=Request)
    mock_request.state.licenses = [
        {"uuid": "test-licence-1", "name": "Test Licence 1"},
        {"uuid": "test-licence-2", "name": "Test Licence 2"}
    ]
    
    assert not is_licence_found(mock_request, "test-licence-3")


def test_is_licence_found_no_licenses():
    mock_request = MagicMock(spec=Request)
    mock_request.state.licenses = None
    
    assert not is_licence_found(mock_request, "test-licence")


def test_get_licences_success():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"uuid": "test-licence-1", "name": "Test Licence 1"},
        {"uuid": "test-licence-2", "name": "Test Licence 2"}
    ]
    
    with patch('httpx.get', return_value=mock_response):
        with patch('middlewares.licence_middleware.URL_API_GATEWAY', 'http://api-gateway'):
            licences = get_licences("test-token")
            
            assert len(licences) == 2
            assert licences[0]["uuid"] == "test-licence-1"
            assert licences[1]["uuid"] == "test-licence-2"


def test_get_licences_failure():
    mock_response = MagicMock()
    mock_response.status_code = 500
    
    with patch('httpx.get', return_value=mock_response):
        with patch('middlewares.licence_middleware.URL_API_GATEWAY', 'http://api-gateway'):
            with pytest.raises(HTTPException) as exc:
                get_licences("test-token")
            
            assert exc.value.status_code == 500
            assert exc.value.detail == "Licences request failed"


def test_filter_licences_active():
    current_time = int(datetime.now(timezone.utc).timestamp())
    licences = [
        {
            "uuid": "licence-1",
            "type_uuid": "type-1",
            "name": "Active Licence 1",
            "iat": current_time - 3600,  # Issued 1 hour ago
            "exp": current_time + 3600,  # Expires in 1 hour
            "entity_uuid": "entity-1",
            "other_field": "value"
        },
        {
            "uuid": "licence-2",
            "type_uuid": "type-2",
            "name": "Active Licence 2",
            "iat": current_time - 7200,  # Issued 2 hours ago
            "exp": current_time + 7200,  # Expires in 2 hours
            "entity_uuid": "entity-2",
            "other_field": "value"
        }
    ]
    
    filtered = filter_licences(licences)
    
    assert len(filtered) == 2
    assert filtered[0]["uuid"] == "licence-1"
    assert filtered[1]["uuid"] == "licence-2"
    assert "other_field" not in filtered[0]
    assert "other_field" not in filtered[1]


def test_filter_licences_expired():
    current_time = int(datetime.now(timezone.utc).timestamp())
    licences = [
        {
            "uuid": "licence-1",
            "type_uuid": "type-1",
            "name": "Expired Licence",
            "iat": current_time - 7200,  # Issued 2 hours ago
            "exp": current_time - 3600,  # Expired 1 hour ago
            "entity_uuid": "entity-1"
        },
        {
            "uuid": "licence-2",
            "type_uuid": "type-2",
            "name": "Active Licence",
            "iat": current_time - 3600,  # Issued 1 hour ago
            "exp": current_time + 3600,  # Expires in 1 hour
            "entity_uuid": "entity-2"
        }
    ]
    
    filtered = filter_licences(licences)
    
    assert len(filtered) == 1
    assert filtered[0]["uuid"] == "licence-2"


def test_filter_licences_not_yet_valid():
    current_time = int(datetime.now(timezone.utc).timestamp())
    licences = [
        {
            "uuid": "licence-1",
            "type_uuid": "type-1",
            "name": "Future Licence",
            "iat": current_time + 3600,  # Will be issued in 1 hour
            "exp": current_time + 7200,  # Will expire in 2 hours
            "entity_uuid": "entity-1"
        },
        {
            "uuid": "licence-2",
            "type_uuid": "type-2",
            "name": "Active Licence",
            "iat": current_time - 3600,  # Issued 1 hour ago
            "exp": current_time + 3600,  # Expires in 1 hour
            "entity_uuid": "entity-2"
        }
    ]
    
    filtered = filter_licences(licences)
    
    assert len(filtered) == 1
    assert filtered[0]["uuid"] == "licence-2"


def test_prepare_licences():
    licences = [
        {"uuid": "licence-1", "name": "Licence 1"},
        {"uuid": "licence-2", "name": "Licence 2"}
    ]
    filtered_licences = [
        {"uuid": "licence-1", "name": "Licence 1"}
    ]
    
    with patch('middlewares.licence_middleware.get_licences', return_value=licences):
        with patch('middlewares.licence_middleware.filter_licences', return_value=filtered_licences):
            result = prepare_licences("test-token")
            
            assert result == filtered_licences


def test_refresh_cache_token():
    mock_request = MagicMock(spec=Request)
    mock_request.state.token = "test-token"
    mock_request.state.licenses = [{"uuid": "licence-1"}]
    
    cached_token = {"sub": "user-123"}
    expected_token = {"sub": "user-123", "licenses": [{"uuid": "licence-1"}]}
    
    with patch('middlewares.licence_middleware.read_cache_token', return_value=cached_token):
        result = refresh_cache_token(mock_request)
        
        assert result == expected_token


def test_refresh_licences():
    mock_request = MagicMock(spec=Request)
    mock_request.state.token = "test-token"
    
    licences = [{"uuid": "licence-1"}]
    
    with patch('middlewares.licence_middleware.prepare_licences', return_value=licences):
        with patch('middlewares.licence_middleware.refresh_cache_token', return_value={}):
            with patch('middlewares.licence_middleware.write_cache_token'):
                refresh_licences(mock_request)
                
                assert mock_request.state.licenses == licences


def test_check_licence_found():
    mock_request = MagicMock(spec=Request)
    mock_request.state.licenses = [{"uuid": "licence-1"}]
    
    with patch('middlewares.licence_middleware.is_licence_found', return_value=True):
        # Should not raise an exception
        check_licence(mock_request, "licence-1")


def test_check_licence_not_found_then_found():
    mock_request = MagicMock(spec=Request)
    
    # First call returns False, second call returns True
    with patch('middlewares.licence_middleware.is_licence_found', side_effect=[False, True]):
        with patch('middlewares.licence_middleware.refresh_licences'):
            # Should not raise an exception
            check_licence(mock_request, "licence-1")


def test_check_licence_not_found():
    mock_request = MagicMock(spec=Request)
    
    with patch('middlewares.licence_middleware.is_licence_found', return_value=False):
        with patch('middlewares.licence_middleware.refresh_licences'):
            with pytest.raises(HTTPException) as exc:
                check_licence(mock_request, "licence-1")
            
            assert exc.value.status_code == 403
            assert exc.value.detail == "Licence not found"


def test_extract_entity_found():
    mock_request = MagicMock(spec=Request)
    mock_request.state.licenses = [
        {"uuid": "licence-1", "entity_uuid": "entity-1"},
        {"uuid": "licence-2", "entity_uuid": "entity-2"}
    ]
    mock_request.state.licence_uuid = "licence-1"
    
    entity_uuid = extract_entity(mock_request)
    
    assert entity_uuid == "entity-1"


def test_extract_entity_not_found():
    mock_request = MagicMock(spec=Request)
    mock_request.state.licenses = [
        {"uuid": "licence-1", "entity_uuid": "entity-1"},
        {"uuid": "licence-2", "entity_uuid": "entity-2"}
    ]
    mock_request.state.licence_uuid = "licence-3"
    
    with pytest.raises(HTTPException) as exc:
        extract_entity(mock_request)
    
    assert exc.value.status_code == 500
    assert exc.value.detail == "Entity not found"


@pytest.mark.asyncio
async def test_licence_verification_middleware_protected_path_valid_licence():
    # Mock request with valid licence
    mock_request = MagicMock(spec=Request)
    mock_request.url.path = "/api/v1/items"
    mock_request.headers = {"X-License-Key": "test-licence"}
    mock_request.state.licenses = [
        {"uuid": "test-licence", "entity_uuid": "entity-1"}
    ]
    
    # Mock next middleware
    mock_call_next = AsyncMock()
    mock_call_next.return_value = JSONResponse(content={"message": "success"})
    
    # Create middleware instance
    middleware = LicenceVerificationMiddleware(None)
    
    # Mock all the necessary functions
    with patch('middlewares.licence_middleware.is_unprotected_path', return_value=False):
        with patch('middlewares.licence_middleware.is_unlicensed_path', return_value=False):
            with patch('middlewares.licence_middleware.check_headers_licence'):
                with patch('middlewares.licence_middleware.extract_licence', return_value="test-licence"):
                    with patch('middlewares.licence_middleware.check_licence'):
                        with patch('middlewares.licence_middleware.extract_entity', return_value="entity-1"):
                            with patch('logging.info'):
                                # Call middleware
                                response = await middleware.dispatch(mock_request, mock_call_next)
                                
                                # Verify response
                                assert response.status_code == 200
                                assert response.body == b'{"message":"success"}'
                                
                                # Verify next middleware was called
                                mock_call_next.assert_called_once_with(mock_request)
                                
                                # Verify state was updated
                                assert mock_request.state.licence_uuid == "test-licence"
                                assert mock_request.state.entity_uuid == "entity-1"


@pytest.mark.asyncio
async def test_licence_verification_middleware_unprotected_path():
    # Mock request for unprotected path
    mock_request = MagicMock(spec=Request)
    mock_request.url.path = "/docs"
    
    # Mock next middleware
    mock_call_next = AsyncMock()
    mock_call_next.return_value = JSONResponse(content={"message": "success"})
    
    # Create middleware instance
    middleware = LicenceVerificationMiddleware(None)
    
    # Mock is_unprotected_path to return True
    with patch('middlewares.licence_middleware.is_unprotected_path', return_value=True):
        with patch('logging.info'):
            # Call middleware
            response = await middleware.dispatch(mock_request, mock_call_next)
            
            # Verify response
            assert response.status_code == 200
            assert response.body == b'{"message":"success"}'
            
            # Verify next middleware was called without licence verification
            mock_call_next.assert_called_once_with(mock_request)


@pytest.mark.asyncio
async def test_licence_verification_middleware_unlicensed_path():
    # Mock request for unlicensed path
    mock_request = MagicMock(spec=Request)
    mock_request.url.path = "/health"
    
    # Mock next middleware
    mock_call_next = AsyncMock()
    mock_call_next.return_value = JSONResponse(content={"message": "success"})
    
    # Create middleware instance
    middleware = LicenceVerificationMiddleware(None)
    
    # Mock path checks
    with patch('middlewares.licence_middleware.is_unprotected_path', return_value=False):
        with patch('middlewares.licence_middleware.is_unlicensed_path', return_value=True):
            with patch('logging.info'):
                # Call middleware
                response = await middleware.dispatch(mock_request, mock_call_next)
                
                # Verify response
                assert response.status_code == 200
                assert response.body == b'{"message":"success"}'
                
                # Verify next middleware was called without licence verification
                mock_call_next.assert_called_once_with(mock_request)


@pytest.mark.asyncio
async def test_licence_verification_middleware_invalid_licence():
    # Mock request with invalid licence
    mock_request = MagicMock(spec=Request)
    mock_request.url.path = "/api/v1/items"
    mock_request.headers = {"X-License-Key": "invalid-licence"}
    
    # Create middleware instance
    middleware = LicenceVerificationMiddleware(None)
    
    # Mock functions to raise an exception
    with patch('middlewares.licence_middleware.is_unprotected_path', return_value=False):
        with patch('middlewares.licence_middleware.is_unlicensed_path', return_value=False):
            with patch('middlewares.licence_middleware.check_headers_licence', side_effect=HTTPException(status_code=403, detail="Invalid licence")):
                with patch('logging.info'):
                    # Call middleware
                    response = await middleware.dispatch(mock_request, AsyncMock())
                    
                    # Verify response
                    assert response.status_code == 403
                    assert b"Invalid licence" in response.body