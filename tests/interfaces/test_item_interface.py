import pytest
from typing import List, Dict, Any

from interfaces.item_interface import ItemRepository
from models.recipe_model import RecipeWrite


class TestItemRepository(ItemRepository):
    """
    A concrete implementation of the ItemRepository interface for testing.
    """
    def __init__(self):
        self.items = {}
        self.is_closed = False

    def create_item(self, item_create: RecipeWrite) -> str:
        item_id = "test-uuid"
        self.items[item_id] = item_create
        return item_id

    def get_item(self, item_id: str) -> Dict[str, Any]:
        if item_id in self.items:
            return {"uuid": item_id, "name": self.items[item_id].name}
        return None

    def list_items(self) -> List[Dict[str, Any]]:
        return [{"uuid": item_id, "name": item.name} for item_id, item in self.items.items()]

    def update_item(self, item_id: str, item_update: RecipeWrite) -> None:
        if item_id in self.items:
            self.items[item_id] = item_update

    def delete_item(self, item_id: str) -> None:
        if item_id in self.items:
            del self.items[item_id]

    def close(self) -> None:
        self.is_closed = True


def test_item_repository_interface():
    """
    Test that a concrete implementation of ItemRepository can be created
    and that it implements all the required methods.
    """
    # Create a concrete implementation
    repo = TestItemRepository()

    # Test create_item
    item = RecipeWrite(name="Test Item")
    item_id = repo.create_item(item)
    assert item_id == "test-uuid"

    # Test get_item
    retrieved_item = repo.get_item(item_id)
    assert retrieved_item["uuid"] == item_id
    assert retrieved_item["name"] == "Test Item"

    # Test list_items
    items = repo.list_items()
    assert len(items) == 1
    assert items[0]["uuid"] == item_id
    assert items[0]["name"] == "Test Item"

    # Test update_item
    updated_item = RecipeWrite(name="Updated Item")
    repo.update_item(item_id, updated_item)
    retrieved_item = repo.get_item(item_id)
    assert retrieved_item["name"] == "Updated Item"

    # Test delete_item
    repo.delete_item(item_id)
    assert repo.get_item(item_id) is None

    # Test close
    repo.close()
    assert repo.is_closed


def test_item_repository_abstract_methods():
    """
    Test that ItemRepository cannot be instantiated directly
    because it has abstract methods.
    """
    with pytest.raises(TypeError) as exc:
        ItemRepository()

    assert "Can't instantiate abstract class ItemRepository" in str(exc.value)
    assert "abstract methods" in str(exc.value)
