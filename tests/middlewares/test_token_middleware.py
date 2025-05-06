import pytest
import time
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi import HTTPException, Request
from starlette.responses import JSONResponse

from middlewares.token_middleware import (
    generate_state_info, is_token_valid_audience, is_token_active,
    read_cache_token, write_cache_token, introspect_token, prepare_cache_token,
    get_token_info, delete_cache_token, is_headers_token_present, extract_token,
    refresh_cache_token, store_token_info_in_state, check_headers_token,
    check_token, TokenVerificationMiddleware
)


def test_generate_state_info():
    token_info = {
        "sub": "user-123",
        "preferred_username": "testuser",
        "email": "test@example.com",
        "aud": ["api-recipe", "other-api"],
        "resource_access": {"api-recipe": ["admin"]},
        "cached_time": 1234567890
    }
    
    state_info = generate_state_info(token_info)
    
    assert state_info["user_uuid"] == "user-123"
    assert state_info["user_display_name"] == "testuser"
    assert state_info["user_email"] == "test@example.com"
    assert state_info["user_audiences"] == ["api-recipe", "other-api"]
    assert state_info["user_roles"] == {"api-recipe": ["admin"]}
    assert state_info["cached_time"] == 1234567890


def test_is_token_valid_audience_valid():
    with patch('middlewares.token_middleware.API_NAME', 'api-recipe'):
        token_info = {"aud": ["api-recipe", "other-api"]}
        assert is_token_valid_audience(token_info)


def test_is_token_valid_audience_invalid():
    with patch('middlewares.token_middleware.API_NAME', 'api-recipe'):
        token_info = {"aud": ["other-api"]}
        assert not is_token_valid_audience(token_info)


def test_is_token_active_valid():
    current_time = int(time.time())
    token_info = {
        "iat": current_time - 3600,  # Issued 1 hour ago
        "exp": current_time + 3600   # Expires in 1 hour
    }
    
    assert is_token_active(token_info)


def test_is_token_active_expired():
    current_time = int(time.time())
    token_info = {
        "iat": current_time - 7200,  # Issued 2 hours ago
        "exp": current_time - 3600   # Expired 1 hour ago
    }
    
    assert not is_token_active(token_info)


def test_is_token_active_not_yet_valid():
    current_time = int(time.time())
    token_info = {
        "iat": current_time + 3600,  # Will be issued in 1 hour
        "exp": current_time + 7200   # Will expire in 2 hours
    }
    
    assert not is_token_active(token_info)


def test_is_token_active_missing_fields():
    token_info = {}
    assert not is_token_active(token_info)
    
    token_info = {"iat": 123456789}
    assert not is_token_active(token_info)
    
    token_info = {"exp": 123456789}
    assert not is_token_active(token_info)


def test_read_cache_token_exists():
    mock_redis = MagicMock()
    mock_redis.get.return_value = "{'sub': 'user-123'}"
    
    with patch('middlewares.token_middleware.r', mock_redis):
        result = read_cache_token("test-token")
        
        mock_redis.get.assert_called_once_with("test-token")
        assert result == {'sub': 'user-123'}


def test_read_cache_token_not_exists():
    mock_redis = MagicMock()
    mock_redis.get.return_value = None
    
    with patch('middlewares.token_middleware.r', mock_redis):
        result = read_cache_token("test-token")
        
        mock_redis.get.assert_called_once_with("test-token")
        assert result is None


def test_write_cache_token():
    mock_redis = MagicMock()
    current_time = int(time.time())
    token_info = {
        "sub": "user-123",
        "exp": current_time + 3600  # Expires in 1 hour
    }
    
    with patch('middlewares.token_middleware.r', mock_redis):
        write_cache_token("test-token", token_info)
        
        mock_redis.set.assert_called_once()
        # Check that the token and token_info were passed to set
        args, kwargs = mock_redis.set.call_args
        assert args[0] == "test-token"
        assert args[1] == str(token_info)
        # Check that the expiration time was set
        assert kwargs.get('ex') is not None


def test_introspect_token_success():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"active": True, "sub": "user-123"}
    
    with patch('httpx.post', return_value=mock_response):
        with patch('middlewares.token_middleware.KEYCLOAK_HOST', 'http://keycloak'):
            with patch('middlewares.token_middleware.KEYCLOAK_REALM', 'test-realm'):
                with patch('middlewares.token_middleware.KEYCLOAK_CLIENT_ID', 'test-client'):
                    with patch('middlewares.token_middleware.KEYCLOAK_CLIENT_SECRET', 'test-secret'):
                        result = introspect_token("test-token")
                        
                        assert result == {"active": True, "sub": "user-123"}


def test_introspect_token_failure():
    mock_response = MagicMock()
    mock_response.status_code = 500
    
    with patch('httpx.post', return_value=mock_response):
        with patch('middlewares.token_middleware.KEYCLOAK_HOST', 'http://keycloak'):
            with patch('middlewares.token_middleware.KEYCLOAK_REALM', 'test-realm'):
                with patch('middlewares.token_middleware.KEYCLOAK_CLIENT_ID', 'test-client'):
                    with patch('middlewares.token_middleware.KEYCLOAK_CLIENT_SECRET', 'test-secret'):
                        with pytest.raises(HTTPException) as exc:
                            introspect_token("test-token")
                        
                        assert exc.value.status_code == 500
                        assert exc.value.detail == "Keycloak introspection failed"


def test_prepare_cache_token():
    token_info = {"sub": "user-123"}
    
    with patch('time.time', return_value=1234567890):
        result = prepare_cache_token(token_info)
        
        assert result["cached_time"] == 1234567890
        assert result["sub"] == "user-123"


def test_get_token_info_from_cache():
    cached_token = {"sub": "user-123", "cached_time": 1234567890}
    
    with patch('middlewares.token_middleware.read_cache_token', return_value=cached_token):
        result = get_token_info("test-token")
        
        assert result == cached_token


def test_get_token_info_from_introspection():
    introspected_token = {"sub": "user-123", "active": True}
    cached_token = {"sub": "user-123", "active": True, "cached_time": 1234567890}
    
    with patch('middlewares.token_middleware.read_cache_token', return_value=None):
        with patch('middlewares.token_middleware.introspect_token', return_value=introspected_token):
            with patch('middlewares.token_middleware.prepare_cache_token', return_value=cached_token):
                with patch('middlewares.token_middleware.write_cache_token') as mock_write:
                    result = get_token_info("test-token")
                    
                    assert result == introspected_token
                    mock_write.assert_called_once_with("test-token", cached_token)


def test_delete_cache_token():
    mock_redis = MagicMock()
    
    with patch('middlewares.token_middleware.r', mock_redis):
        delete_cache_token("test-token")
        
        mock_redis.delete.assert_called_once_with("test-token")


def test_is_headers_token_present_valid():
    mock_request = MagicMock(spec=Request)
    mock_request.headers = {"Authorization": "Bearer test-token"}
    
    assert is_headers_token_present(mock_request)


def test_is_headers_token_present_missing():
    mock_request = MagicMock(spec=Request)
    mock_request.headers = {}
    
    assert not is_headers_token_present(mock_request)


def test_is_headers_token_present_invalid_format():
    mock_request = MagicMock(spec=Request)
    mock_request.headers = {"Authorization": "InvalidFormat test-token"}
    
    assert not is_headers_token_present(mock_request)


def test_extract_token():
    mock_request = MagicMock(spec=Request)
    mock_request.headers = {"Authorization": "Bearer test-token"}
    
    token = extract_token(mock_request)
    
    assert token == "test-token"


def test_check_headers_token_valid():
    mock_request = MagicMock(spec=Request)
    mock_request.headers = {"Authorization": "Bearer test-token"}
    
    with patch('middlewares.token_middleware.is_headers_token_present', return_value=True):
        # Should not raise an exception
        check_headers_token(mock_request)


def test_check_headers_token_invalid():
    mock_request = MagicMock(spec=Request)
    mock_request.headers = {}
    
    with patch('middlewares.token_middleware.is_headers_token_present', return_value=False):
        with pytest.raises(HTTPException) as exc:
            check_headers_token(mock_request)
        
        assert exc.value.status_code == 401
        assert exc.value.detail == "Token manquant ou invalide"


def test_check_token_valid():
    token_info = {"active": True}
    
    with patch('middlewares.token_middleware.is_token_active', return_value=True):
        with patch('middlewares.token_middleware.is_token_valid_audience', return_value=True):
            # Should not raise an exception
            check_token(token_info)


def test_check_token_inactive():
    token_info = {"active": False}
    
    with patch('middlewares.token_middleware.is_token_active', return_value=False):
        with pytest.raises(HTTPException) as exc:
            check_token(token_info)
        
        assert exc.value.status_code == 401
        assert exc.value.detail == "Token is not active"


def test_check_token_invalid_audience():
    token_info = {"active": True}
    
    with patch('middlewares.token_middleware.is_token_active', return_value=True):
        with patch('middlewares.token_middleware.is_token_valid_audience', return_value=False):
            with pytest.raises(HTTPException) as exc:
                check_token(token_info)
            
            assert exc.value.status_code == 401
            assert exc.value.detail == "Token is not valid for this audience"


def test_store_token_info_in_state():
    mock_request = MagicMock(spec=Request)
    state_token_info = {
        "user_uuid": "user-123",
        "user_display_name": "testuser",
        "user_email": "test@example.com",
        "user_audiences": ["api-recipe"],
        "user_roles": {"api-recipe": ["admin"]},
        "cached_time": 1234567890
    }
    
    with patch('middlewares.token_middleware.extract_token', return_value="test-token"):
        store_token_info_in_state(state_token_info, mock_request)
        
        assert mock_request.state.token_info == state_token_info
        assert mock_request.state.user_uuid == "user-123"
        assert mock_request.state.token == "test-token"


@pytest.mark.asyncio
async def test_token_verification_middleware_protected_path_valid_token():
    # Mock request with valid token
    mock_request = MagicMock(spec=Request)
    mock_request.url.path = "/api/v1/items"
    mock_request.headers = {"Authorization": "Bearer test-token"}
    
    # Mock next middleware
    mock_call_next = AsyncMock()
    mock_call_next.return_value = JSONResponse(content={"message": "success"})
    
    # Mock token info
    token_info = {
        "sub": "user-123",
        "preferred_username": "testuser",
        "email": "test@example.com",
        "aud": ["api-recipe"],
        "resource_access": {"api-recipe": ["admin"]},
        "exp": int(time.time()) + 3600
    }
    
    # Create middleware instance
    middleware = TokenVerificationMiddleware(None)
    
    # Mock all the necessary functions
    with patch('middlewares.token_middleware.is_unprotected_path', return_value=False):
        with patch('middlewares.token_middleware.check_headers_token'):
            with patch('middlewares.token_middleware.extract_token', return_value="test-token"):
                with patch('middlewares.token_middleware.get_token_info', return_value=token_info):
                    with patch('middlewares.token_middleware.check_token'):
                        with patch('middlewares.token_middleware.generate_state_info') as mock_generate:
                            with patch('middlewares.token_middleware.store_token_info_in_state'):
                                with patch('logging.info'):
                                    # Call middleware
                                    response = await middleware.dispatch(mock_request, mock_call_next)
                                    
                                    # Verify response
                                    assert response.status_code == 200
                                    assert response.body == b'{"message":"success"}'
                                    
                                    # Verify next middleware was called
                                    mock_call_next.assert_called_once_with(mock_request)


@pytest.mark.asyncio
async def test_token_verification_middleware_unprotected_path():
    # Mock request for unprotected path
    mock_request = MagicMock(spec=Request)
    mock_request.url.path = "/docs"
    
    # Mock next middleware
    mock_call_next = AsyncMock()
    mock_call_next.return_value = JSONResponse(content={"message": "success"})
    
    # Create middleware instance
    middleware = TokenVerificationMiddleware(None)
    
    # Mock is_unprotected_path to return True
    with patch('middlewares.token_middleware.is_unprotected_path', return_value=True):
        with patch('logging.info'):
            # Call middleware
            response = await middleware.dispatch(mock_request, mock_call_next)
            
            # Verify response
            assert response.status_code == 200
            assert response.body == b'{"message":"success"}'
            
            # Verify next middleware was called without token verification
            mock_call_next.assert_called_once_with(mock_request)


@pytest.mark.asyncio
async def test_token_verification_middleware_invalid_token():
    # Mock request with invalid token
    mock_request = MagicMock(spec=Request)
    mock_request.url.path = "/api/v1/items"
    mock_request.headers = {"Authorization": "Bearer invalid-token"}
    
    # Create middleware instance
    middleware = TokenVerificationMiddleware(None)
    
    # Mock functions to raise an exception
    with patch('middlewares.token_middleware.is_unprotected_path', return_value=False):
        with patch('middlewares.token_middleware.check_headers_token', side_effect=HTTPException(status_code=401, detail="Invalid token")):
            with patch('logging.info'):
                # Call middleware
                response = await middleware.dispatch(mock_request, AsyncMock())
                
                # Verify response
                assert response.status_code == 401
                assert b"Invalid token" in response.body