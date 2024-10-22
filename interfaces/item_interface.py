from abc import ABC, abstractmethod
from typing import List
from models.item_model import Item, ItemCreate

class ItemRepository(ABC):

    @abstractmethod
    def create_item(self, item_create: Item) -> ItemCreate:
        pass

    @abstractmethod
    def get_item(self, item_id: int) -> ItemCreate:
        pass

    @abstractmethod
    def list_items(self) -> List[ItemCreate]:
        pass

    @abstractmethod
    def update_item(self, item_id: int, item_update: Item) -> ItemCreate:
        pass

    @abstractmethod
    def delete_item(self, item_id: int) -> None:
        pass