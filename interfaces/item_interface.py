from abc import ABC, abstractmethod
from typing import List
from models.recipe_model import RecipeWrite

class ItemRepository(ABC):

    @abstractmethod
    def create_item(self, item_create: RecipeWrite):
        pass

    @abstractmethod
    def get_item(self, item_id: str):
        pass

    @abstractmethod
    def list_items(self):
        pass

    @abstractmethod
    def update_item(self, item_id: str, item_update: RecipeWrite):
        pass

    @abstractmethod
    def delete_item(self, item_id: str):
        pass

    @abstractmethod
    def close(self):
        pass
