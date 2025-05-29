from abc import ABC, abstractmethod
from typing import List
from models.recipe_model import RecipeWrite

class RecipeRepository(ABC):

    @abstractmethod
    def create_recipe(self, recipe_create: RecipeWrite):
        pass

    @abstractmethod
    def get_recipe(self, recipe_id: str):
        pass

    @abstractmethod
    def list_recipes(self):
        pass

    @abstractmethod
    def update_recipe(self, recipe_id: str, recipe_update: RecipeWrite):
        pass

    @abstractmethod
    def delete_recipe(self, recipe_id: str):
        pass

    @abstractmethod
    def close(self):
        pass