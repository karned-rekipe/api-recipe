import pytest
from unittest.mock import patch, MagicMock, AsyncMock
import logging

from decorators.check_permission import check_roles, check_permissions
from fastapi import HTTPException, status, Request


def test_check_roles_sufficient_permissions():
    user_roles = {'api-recipe': ['admin', 'editor']}
    required_permissions = ['editor']

    check_roles(user_roles, required_permissions)


def test_check_roles_insufficient_permissions():
    user_roles = {'api-recipe': ['reader']}
    required_permissions = ['editor', 'writer']

    with pytest.raises(HTTPException) as e:
        check_roles(user_roles, required_permissions)

    assert e.value.status_code == status.HTTP_403_FORBIDDEN
    assert "Insufficient permissions !" in str(e.value.detail)
    assert "Need : api-recipe/editor, api-recipe/writer" in str(e.value.detail)
    assert "Got : api-recipe/reader" in str(e.value.detail)


def test_check_roles_with_formatted_permissions():
    user_roles = {'api-recipe': ['admin']}
    required_permissions = ['api-recipe/admin']  # Already formatted permission

    # This should not raise an exception
    check_roles(user_roles, required_permissions)


def test_check_roles_with_dict_roles():
    user_roles = {'api-recipe': {'roles': ['admin', 'editor']}}
    required_permissions = ['admin']

    # This should not raise an exception
    check_roles(user_roles, required_permissions)


def test_check_roles_with_other_format():
    user_roles = {'api-recipe': 'some-other-format'}
    required_permissions = ['roles']

    # This should not raise an exception
    check_roles(user_roles, required_permissions)


@pytest.mark.asyncio
async def test_check_permissions_decorator_sufficient_permissions():
    # Create a mock request with sufficient permissions
    mock_request = MagicMock(spec=Request)
    mock_request.state.token_info = {
        'user_roles': {'api-recipe': ['admin', 'editor']}
    }

    # Create a mock endpoint function
    mock_endpoint = AsyncMock(return_value={"message": "success"})

    # Apply the decorator
    decorated_endpoint = check_permissions(['editor'])(mock_endpoint)

    # Mock logging.info to avoid actual logging
    with patch('logging.info'):
        # Call the decorated endpoint
        result = await decorated_endpoint(mock_request, param1="test")

        # Verify the endpoint was called with the correct parameters
        mock_endpoint.assert_called_once_with(mock_request, param1="test")

        # Verify the result
        assert result == {"message": "success"}


@pytest.mark.asyncio
async def test_check_permissions_decorator_insufficient_permissions():
    # Create a mock request with insufficient permissions
    mock_request = MagicMock(spec=Request)
    mock_request.state.token_info = {
        'user_roles': {'api-recipe': ['reader']}
    }

    # Create a mock endpoint function
    mock_endpoint = AsyncMock(return_value={"message": "success"})

    # Apply the decorator
    decorated_endpoint = check_permissions(['admin', 'editor'])(mock_endpoint)

    # Mock logging.info to avoid actual logging
    with patch('logging.info'):
        # Call the decorated endpoint and expect an exception
        with pytest.raises(HTTPException) as e:
            await decorated_endpoint(mock_request)

        # Verify the exception details
        assert e.value.status_code == status.HTTP_403_FORBIDDEN
        assert "Insufficient permissions !" in str(e.value.detail)

        # Verify the endpoint was not called
        mock_endpoint.assert_not_called()
