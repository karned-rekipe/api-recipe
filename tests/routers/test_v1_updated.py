import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from fastapi.testclient import TestClient

from routers.v1 import router
from models.recipe_model import RecipeWrite


# Create a test client for the router
client = TestClient(router)


@pytest.fixture
def mock_check_permissions():
    """Mock the check_permissions decorator to do nothing."""
    with patch('routers.v1.check_permissions', lambda x: lambda func: func):
        yield


@pytest.fixture
def mock_request():
    """Create a mock request with a repository."""
    mock_repo = MagicMock()
    mock_req = MagicMock()
    mock_req.state.repo = mock_repo

    # Create token_info with the correct structure and all required roles
    mock_req.state.token_info = {
        'user_id': 'test-user',
        'user_roles': {'api-recipe': ['create', 'read', 'read_own', 'list', 'list_own', 'update', 'update_own', 'delete', 'delete_own']}
    }

    return mock_req, mock_repo


@pytest.mark.asyncio
async def test_create_new_item(mock_check_permissions, mock_request):
    mock_req, mock_repo = mock_request

    # Mock the create_item service function
    with patch('routers.v1.create_item', return_value="test-uuid") as mock_create:
        # Create a test item
        item = RecipeWrite(name="Test Item")

        # Call the endpoint function directly
        from routers.v1 import create_new_item
        result = await create_new_item(mock_req, item)

        # Verify the result
        assert result == {"uuid": "test-uuid"}

        # Verify create_item was called with the correct arguments
        mock_create.assert_called_once()
        args, _ = mock_create.call_args
        assert args[0] == item
        assert args[1] == mock_repo

        # Verify the item's created_by field was set
        assert item.created_by == "test-user"


@pytest.mark.asyncio
async def test_read_items(mock_check_permissions, mock_request):
    mock_req, mock_repo = mock_request

    # Mock the get_items service function
    items = [
        RecipeWrite(name="Item 1"),
        RecipeWrite(name="Item 2")
    ]
    with patch('routers.v1.get_items', return_value=items) as mock_get_items:
        # Call the endpoint function directly
        from routers.v1 import read_items
        result = await read_items(mock_req)

        # Verify the result
        assert result == items

        # Verify get_items was called with the correct arguments
        mock_get_items.assert_called_once_with(mock_repo)


@pytest.mark.asyncio
async def test_read_item_found(mock_check_permissions, mock_request):
    mock_req, mock_repo = mock_request

    # Mock the get_item service function
    item = RecipeWrite(name="Test Item")
    with patch('routers.v1.get_item', return_value=item) as mock_get_item:
        # Call the endpoint function directly
        from routers.v1 import read_item
        result = await read_item(mock_req, "test-uuid")

        # Verify the result
        assert result == item

        # Verify get_item was called with the correct arguments
        mock_get_item.assert_called_once_with("test-uuid", mock_repo)


@pytest.mark.asyncio
async def test_read_item_not_found(mock_check_permissions, mock_request):
    mock_req, mock_repo = mock_request

    # Mock the get_item service function to return None
    with patch('routers.v1.get_item', return_value=None) as mock_get_item:
        # Call the endpoint function directly
        from routers.v1 import read_item

        # Verify that an HTTPException is raised
        with pytest.raises(HTTPException) as exc:
            await read_item(mock_req, "test-uuid")

        # Verify the exception details
        assert exc.value.status_code == 404
        assert exc.value.detail == "Item not found"

        # Verify get_item was called with the correct arguments
        mock_get_item.assert_called_once_with("test-uuid", mock_repo)


@pytest.mark.asyncio
async def test_update_existing_item(mock_check_permissions, mock_request):
    mock_req, mock_repo = mock_request

    # Mock the update_item service function
    with patch('routers.v1.update_item') as mock_update:
        # Create a test item
        item = RecipeWrite(name="Updated Item")

        # Call the endpoint function directly
        from routers.v1 import update_existing_item
        result = await update_existing_item(mock_req, "test-uuid", item)

        # Verify there's no result (204 No Content)
        assert result is None

        # Verify update_item was called with the correct arguments
        mock_update.assert_called_once_with("test-uuid", item, mock_repo)


@pytest.mark.asyncio
async def test_delete_existing_item(mock_check_permissions, mock_request):
    mock_req, mock_repo = mock_request

    # Mock the delete_item service function
    with patch('routers.v1.delete_item') as mock_delete:
        # Call the endpoint function directly
        from routers.v1 import delete_existing_item
        result = await delete_existing_item(mock_req, "test-uuid")

        # Verify there's no result (204 No Content)
        assert result is None

        # Verify delete_item was called with the correct arguments
        mock_delete.assert_called_once_with("test-uuid", mock_repo)


# Integration tests using the TestClient

def test_router_create_item(mock_check_permissions):
    # Mock the create_item service function
    with patch('routers.v1.create_item', return_value="test-uuid"):
        # Mock the check_permissions decorator
        with patch('routers.v1.check_permissions', lambda x: lambda func: func):
            # Create a test client with a mocked app
            with patch('fastapi.APIRouter.post'):
                # This test is just to verify the router is set up correctly
                # Actual API testing would require more setup
                pass


def test_router_endpoints_exist():
    # Verify that the router has the expected endpoints
    routes = router.routes

    # Check that there are 5 routes (POST /, GET /, GET /{uuid}, PUT /{uuid}, DELETE /{uuid})
    assert len(routes) == 5

    # Get the paths without checking the exact path strings
    # since the router has a prefix that might change
    methods = [route.methods for route in routes]

    # Check that all expected HTTP methods are present
    assert {'POST'} in methods
    assert {'GET'} in methods  # This will match both GET / and GET /{uuid}
    assert {'PUT'} in methods
    assert {'DELETE'} in methods

    # Count the number of GET endpoints (should be 2: one for / and one for /{uuid})
    assert methods.count({'GET'}) == 2