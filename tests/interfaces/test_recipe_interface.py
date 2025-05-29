import pytest
from typing import List, Dict, Any

from interfaces.recipe_interface import RecipeRepository
from models.recipe_model import RecipeWrite


class TestRecipeRepository(RecipeRepository):
    """
    A concrete implementation of the RecipeRepository interface for testing.
    """
    def __init__(self):
        self.recipes = {}
        self.is_closed = False

    def create_recipe(self, recipe_create: RecipeWrite) -> str:
        recipe_id = "test-uuid"
        self.recipes[recipe_id] = recipe_create
        return recipe_id

    def get_recipe(self, recipe_id: str) -> Dict[str, Any]:
        if recipe_id in self.recipes:
            return {"uuid": recipe_id, "name": self.recipes[recipe_id].name}
        return None

    def list_recipes(self) -> List[Dict[str, Any]]:
        return [{"uuid": recipe_id, "name": recipe.name} for recipe_id, recipe in self.recipes.items()]

    def update_recipe(self, recipe_id: str, recipe_update: RecipeWrite) -> None:
        if recipe_id in self.recipes:
            self.recipes[recipe_id] = recipe_update

    def delete_recipe(self, recipe_id: str) -> None:
        if recipe_id in self.recipes:
            del self.recipes[recipe_id]

    def close(self) -> None:
        self.is_closed = True


def test_recipe_repository_interface():
    """
    Test that a concrete implementation of RecipeRepository can be created
    and that it implements all the required methods.
    """
    # Create a concrete implementation
    repo = TestRecipeRepository()

    # Test create_recipe
    recipe = RecipeWrite(name="Test Recipe")
    recipe_id = repo.create_recipe(recipe)
    assert recipe_id == "test-uuid"

    # Test get_recipe
    retrieved_recipe = repo.get_recipe(recipe_id)
    assert retrieved_recipe["uuid"] == recipe_id
    assert retrieved_recipe["name"] == "Test Recipe"

    # Test list_recipes
    recipes = repo.list_recipes()
    assert len(recipes) == 1
    assert recipes[0]["uuid"] == recipe_id
    assert recipes[0]["name"] == "Test Recipe"

    # Test update_recipe
    updated_recipe = RecipeWrite(name="Updated Recipe")
    repo.update_recipe(recipe_id, updated_recipe)
    retrieved_recipe = repo.get_recipe(recipe_id)
    assert retrieved_recipe["name"] == "Updated Recipe"

    # Test delete_recipe
    repo.delete_recipe(recipe_id)
    assert repo.get_recipe(recipe_id) is None

    # Test close
    repo.close()
    assert repo.is_closed


def test_recipe_repository_abstract_methods():
    """
    Test that RecipeRepository cannot be instantiated directly
    because it has abstract methods.
    """
    with pytest.raises(TypeError) as exc:
        RecipeRepository()

    assert "Can't instantiate abstract class RecipeRepository" in str(exc.value)
    assert "abstract methods" in str(exc.value)