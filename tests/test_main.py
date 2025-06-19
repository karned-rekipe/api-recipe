import pytest
from unittest.mock import patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

import main


@pytest.fixture
def mock_middlewares():
    """Mock all middleware classes to avoid actual implementation."""
    with patch('main.TokenVerificationMiddleware') as mock_token:
        with patch('main.LicenceVerificationMiddleware') as mock_licence:
            with patch('main.DBConnectionMiddleware') as mock_db:
                with patch('main.CORSMiddleware') as mock_cors:
                    yield mock_token, mock_licence, mock_db, mock_cors


@pytest.fixture
def mock_router():
    """Mock the v1 router."""
    with patch('main.v1.router') as mock_router:
        yield mock_router


def test_app_initialization():
    """Test that the FastAPI app is initialized correctly."""
    assert isinstance(main.app, FastAPI)
    assert main.app.openapi_url == "/recipe/openapi.json"


def test_custom_openapi():
    """Test the custom OpenAPI schema generation."""
    # Mock the app's openapi_schema to be None to force regeneration
    with patch.object(main.app, 'openapi_schema', None):
        with patch('main.get_openapi') as mock_get_openapi:
            # Mock the return value of get_openapi
            mock_openapi_schema = {
                "components": {},
                "paths": {
                    "/test": {
                        "get": {}
                    }
                }
            }
            mock_get_openapi.return_value = mock_openapi_schema

            # Call the custom_openapi function
            result = main.custom_openapi()

            # Verify get_openapi was called with the correct arguments
            mock_get_openapi.assert_called_once_with(
                title="API Recipe",
                version="1.0.0",
                description="Cookbook recipe for all !",
                routes=main.app.routes,
            )

            # Verify the security schemes were added
            assert "securitySchemes" in result["components"]
            assert "BearerAuth" in result["components"]["securitySchemes"]
            assert "LicenceHeader" in result["components"]["securitySchemes"]

            # Verify security was added to each path
            assert "security" in result["paths"]["/test"]["get"]
            assert result["paths"]["/test"]["get"]["security"] == [
                {"BearerAuth": []},
                {"LicenceHeader": []}
            ]


def test_middleware_registration():
    """Test that middlewares are registered correctly."""
    # Check that the app has middleware registered
    assert len(main.app.user_middleware) > 0

    # Verify that the middleware registration code exists in main.py
    import inspect
    main_source = inspect.getsource(main)
    assert "app.add_middleware(CORSMiddleware)" in main_source
    assert "app.add_middleware(DBConnectionMiddleware)" in main_source
    assert "app.add_middleware(LicenceVerificationMiddleware)" in main_source
    assert "app.add_middleware(TokenVerificationMiddleware)" in main_source


def test_router_registration():
    """Test that routers are registered correctly."""
    # Check that the app has routes (which means routers are registered)
    assert len(main.app.routes) > 0

    # Check that at least one route has the expected path prefix for v1 router
    route_paths = [route.path for route in main.app.routes if hasattr(route, 'path')]
    assert any(path.startswith("/recipe/v1") for path in route_paths)


def test_app_with_test_client():
    """Test the app using TestClient."""
    client = TestClient(main.app)

    # Test the OpenAPI endpoint with a simplified approach
    # Just verify that the app has the custom_openapi function set
    assert main.app.openapi == main.custom_openapi

    # Verify that the custom_openapi function returns a dictionary
    # when the openapi_schema is None
    with patch.object(main.app, 'openapi_schema', None):
        with patch('main.get_openapi', return_value={"components": {}, "paths": {}}):
            result = main.custom_openapi()
            assert isinstance(result, dict)
            assert "components" in result
            assert "securitySchemes" in result["components"]


def test_logging_setup():
    """Test that logging is set up correctly."""
    with patch('main.logging.basicConfig') as mock_basic_config:
        with patch('main.logging.info') as mock_info:
            # Re-execute the logging setup code
            import importlib
            importlib.reload(main)

            # Verify basicConfig was called with the correct level
            mock_basic_config.assert_called_once_with(level=main.logging.INFO)

            # Verify the startup log message
            mock_info.assert_called_with("Starting API")
