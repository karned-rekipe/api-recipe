import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi import HTTPException, Request
from starlette.responses import JSONResponse

from common_api.middlewares.v1.database_middleware import (
    read_cache_credential, write_cache_credential, get_credential,
    check_repo, DBConnectionMiddleware
)


def test_read_cache_credential_exists():
    mock_redis = MagicMock()
    mock_redis.get.return_value = "{'uri': 'mongodb://localhost:27017'}"
    
    with patch('middlewares.database_middleware.r', mock_redis):
        result = read_cache_credential("test-licence")
        
        mock_redis.get.assert_called_once_with("test-licence_database")
        assert result == {'uri': 'mongodb://localhost:27017'}


def test_read_cache_credential_not_exists():
    mock_redis = MagicMock()
    mock_redis.get.return_value = None
    
    with patch('middlewares.database_middleware.r', mock_redis):
        result = read_cache_credential("test-licence")
        
        mock_redis.get.assert_called_once_with("test-licence_database")
        assert result is None


def test_write_cache_credential():
    mock_redis = MagicMock()
    credential = {'uri': 'mongodb://localhost:27017'}
    
    with patch('middlewares.database_middleware.r', mock_redis):
        write_cache_credential("test-licence", credential)
        
        mock_redis.set.assert_called_once()
        # Check that the key, value, and expiration were passed to set
        args, kwargs = mock_redis.set.call_args
        assert args[0] == "test-licence_database"
        assert args[1] == str(credential)
        assert kwargs.get('ex') == 1800


def test_get_credential_from_cache():
    cached_credential = {'uri': 'mongodb://localhost:27017'}
    
    with patch('middlewares.database_middleware.read_cache_credential', return_value=cached_credential):
        result = get_credential("test-token", "test-licence")
        
        assert result == cached_credential


def test_get_credential_from_api():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'uri': 'mongodb://localhost:27017'}
    
    with patch('middlewares.database_middleware.read_cache_credential', return_value=None):
        with patch('httpx.get', return_value=mock_response):
            with patch('middlewares.database_middleware.URL_API_GATEWAY', 'http://api-gateway'):
                with patch('middlewares.database_middleware.write_cache_credential') as mock_write:
                    result = get_credential("test-token", "test-licence")
                    
                    assert result == {'uri': 'mongodb://localhost:27017'}
                    mock_write.assert_called_once_with("test-licence", {'uri': 'mongodb://localhost:27017'})


def test_get_credential_api_failure():
    mock_response = MagicMock()
    mock_response.status_code = 500
    
    with patch('middlewares.database_middleware.read_cache_credential', return_value=None):
        with patch('httpx.get', return_value=mock_response):
            with patch('middlewares.database_middleware.URL_API_GATEWAY', 'http://api-gateway'):
                with pytest.raises(HTTPException) as exc:
                    get_credential("test-token", "test-licence")
                
                assert exc.value.status_code == 500
                assert exc.value.detail == "Credential request failed"


def test_check_repo_valid():
    repo = MagicMock()
    
    # Should not raise an exception
    check_repo(repo)


def test_check_repo_invalid():
    with pytest.raises(Exception) as exc:
        check_repo(None)
    
    assert str(exc.value) == "DBConnectionMiddleware: Error: No repository found"


@pytest.mark.asyncio
async def test_db_connection_middleware_protected_path_valid_token():
    # Mock request with valid token and licence
    mock_request = MagicMock(spec=Request)
    mock_request.url.path = "/api/v1/items"
    mock_request.state.licence_uuid = "test-licence"
    
    # Mock next middleware
    mock_call_next = AsyncMock()
    mock_call_next.return_value = JSONResponse(content={"message": "success"})
    
    # Mock repository
    mock_repo = MagicMock()
    
    # Create middleware instance
    middleware = DBConnectionMiddleware(None)
    
    # Mock all the necessary functions
    with patch('middlewares.database_middleware.is_unprotected_path', return_value=False):
        with patch('middlewares.database_middleware.extract_token', return_value="test-token"):
            with patch('middlewares.database_middleware.get_credential', return_value={'uri': 'mongodb://localhost:27017'}):
                with patch('middlewares.database_middleware.ItemRepositoryMongo', return_value=mock_repo):
                    with patch('middlewares.database_middleware.check_repo'):
                        with patch('logging.info'):
                            # Call middleware
                            response = await middleware.dispatch(mock_request, mock_call_next)
                            
                            # Verify response
                            assert response.status_code == 200
                            assert response.body == b'{"message":"success"}'
                            
                            # Verify next middleware was called
                            mock_call_next.assert_called_once_with(mock_request)
                            
                            # Verify repository was attached to request state
                            assert mock_request.state.repo == mock_repo


@pytest.mark.asyncio
async def test_db_connection_middleware_unprotected_path():
    # Mock request for unprotected path
    mock_request = MagicMock(spec=Request)
    mock_request.url.path = "/docs"
    
    # Mock next middleware
    mock_call_next = AsyncMock()
    mock_call_next.return_value = JSONResponse(content={"message": "success"})
    
    # Create middleware instance
    middleware = DBConnectionMiddleware(None)
    
    # Mock is_unprotected_path to return True
    with patch('middlewares.database_middleware.is_unprotected_path', return_value=True):
        with patch('logging.info'):
            # Call middleware
            response = await middleware.dispatch(mock_request, mock_call_next)
            
            # Verify response
            assert response.status_code == 200
            assert response.body == b'{"message":"success"}'
            
            # Verify next middleware was called without database connection
            mock_call_next.assert_called_once_with(mock_request)


@pytest.mark.asyncio
async def test_db_connection_middleware_credential_error():
    # Mock request with valid token and licence
    mock_request = MagicMock(spec=Request)
    mock_request.url.path = "/api/v1/items"
    mock_request.state.licence_uuid = "test-licence"
    
    # Create middleware instance
    middleware = DBConnectionMiddleware(None)
    
    # Mock functions to raise an exception
    with patch('middlewares.database_middleware.is_unprotected_path', return_value=False):
        with patch('middlewares.database_middleware.extract_token', return_value="test-token"):
            with patch('middlewares.database_middleware.get_credential', side_effect=HTTPException(status_code=500, detail="Credential error")):
                with patch('logging.info'):
                    # Call middleware
                    response = await middleware.dispatch(mock_request, AsyncMock())
                    
                    # Verify response
                    assert response.status_code == 500
                    assert b"Credential error" in response.body


@pytest.mark.asyncio
async def test_db_connection_middleware_repo_error():
    # Mock request with valid token and licence
    mock_request = MagicMock(spec=Request)
    mock_request.url.path = "/api/v1/items"
    mock_request.state.licence_uuid = "test-licence"
    
    # Create middleware instance
    middleware = DBConnectionMiddleware(None)
    
    # Mock functions to raise an exception
    with patch('middlewares.database_middleware.is_unprotected_path', return_value=False):
        with patch('middlewares.database_middleware.extract_token', return_value="test-token"):
            with patch('middlewares.database_middleware.get_credential', return_value={'uri': 'mongodb://localhost:27017'}):
                with patch('middlewares.database_middleware.ItemRepositoryMongo', return_value=None):
                    with patch('middlewares.database_middleware.check_repo', side_effect=Exception("Repository error")):
                        with patch('logging.info'):
                            # Call middleware
                            response = await middleware.dispatch(mock_request, AsyncMock())
                            
                            # Verify response is a JSONResponse with error details
                            assert isinstance(response, JSONResponse)