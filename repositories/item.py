from typing import List

from pymongo import MongoClient
from models.item import Item, ItemCreate
from interfaces.item import ItemRepository

class ItemRepositoryMongo(ItemRepository):

    def __init__(self, url: str, name: str):
        self.client = MongoClient(url)
        self.db = self.client[name]
        self.collection = self.db["items"]

    def create_item(self, item_create: ItemCreate):
        self.collection.insert_one(dict(item_create))

    def get_item(self, item_id: int) -> Item:
        data = self.collection.find_one({"id": item_id})
        return Item(**data) if data else None

    def list_items(self) -> List[Item]:
        items = self.collection.find()
        return [Item(**item) for item in items]

    def update_item(self, item_id: int, item_update: ItemCreate) -> Item:
        update_data = {"$set": item_update.dict()}
        result = self.collection.update_one({"id": item_id}, update_data)

        if result.matched_count == 0:
            raise ValueError(f"Item with id {item_id} not found")

        updated_item = self.collection.find_one({"id": item_id})
        return Item(**updated_item)

    def delete_item(self, item_id: int) -> None:
        self.collection.delete_one({"id": item_id})