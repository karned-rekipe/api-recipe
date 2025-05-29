from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from services.items_service import create_item, get_items, get_item, update_item, delete_item


def test_create_item_success():
    repository = MagicMock()
    repository.create_item.return_value = "new_id"
    assert create_item("new_item", repository) == "new_id"


def test_create_item_failure():
    repository = MagicMock()
    repository.create_item.side_effect = Exception("An error occurred")
    with pytest.raises(HTTPException):
        create_item("new_item", repository)


def test_create_item_invalid_id():
    repository = MagicMock()
    repository.create_item.return_value = 123
    with pytest.raises(Exception):
        create_item("new_item", repository)


def test_get_items_success():
    repository = MagicMock()
    mock_item = {"uuid": "1", "name": "Item 1"}
    repository.list_items.return_value = [mock_item]
    assert get_items(repository) == [mock_item]


def test_get_items_failure():
    repository = MagicMock()
    repository.list_items.side_effect = Exception("An error occurred")
    with pytest.raises(HTTPException):
        get_items(repository)


def test_get_items_invalid_response():
    repository = MagicMock()
    repository.list_items.return_value = "Invalid response"
    with pytest.raises(Exception):
        get_items(repository)


def test_get_item_success():
    repository = MagicMock()
    mock_item = {"uuid": "1", "name": "Item 1"}
    repository.get_item.return_value = mock_item
    assert get_item("1", repository) == mock_item


def test_get_item_not_found():
    repository = MagicMock()
    repository.get_item.return_value = None
    with pytest.raises(HTTPException) as e:
        get_item("2", repository)
    assert e.value.status_code == 404
    assert e.value.detail == "Item not found"


def test_get_item_failure():
    repository = MagicMock()
    repository.get_item.side_effect = Exception("An error occurred")
    with pytest.raises(HTTPException) as e:
        get_item("1", repository)
    assert e.value.status_code == 500


def test_update_item_success():
    repository = MagicMock()
    item_id = "1"
    item_update = {"name": "Updated Item"}
    update_item(item_id, item_update, repository)
    repository.update_item.assert_called_once_with(item_id, item_update)


def test_update_item_failure():
    repository = MagicMock()
    error_message = "An error occurred while updating the item"
    repository.update_item.side_effect = Exception(error_message)
    with pytest.raises(HTTPException) as e:
        update_item("1", {}, repository)
    assert e.value.status_code == 500
    assert error_message in e.value.detail


def test_delete_item_success():
    repository = MagicMock()
    item_id = "1"
    delete_item(item_id, repository)
    repository.delete_item.assert_called_once_with(item_id)


def test_delete_item_failure():
    repository = MagicMock()
    error_message = "An error occurred while deleting the item"
    repository.delete_item.side_effect = Exception(error_message)
    with pytest.raises(HTTPException) as e:
        delete_item("1", repository)
    assert e.value.status_code == 500
    assert error_message in e.value.detail
