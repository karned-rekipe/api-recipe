from typing import List

from pymongo import MongoClient
from models.item_model import Item, ItemCreate
from interfaces.item_interface import ItemRepository

class ItemRepositoryMongo(ItemRepository):

    def __init__(self, url: str, name: str, collection: str):
        self.url = url
        self.name = name
        self.collection = collection

        self.client = None
        self.db = None

    def __enter__(self):
        self.client = MongoClient(self.url)
        self.db = self.client[self.name]
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def create_item(self, item_create: ItemCreate):
        self.db[self.collection].insert_one(dict(item_create))

    def get_item(self, item_id: int) -> Item:
        data = self.db[self.collection].find_one({"id": item_id})
        return Item(**data) if data else None

    def list_items(self) -> List[Item]:
        items = self.db[self.collection].find()
        return [Item(**item) for item in items]

    def update_item(self, item_id: int, item_update: ItemCreate) -> Item:
        update_data = {"$set": item_update.model_dump()}
        result = self.db[self.collection].update_one({"id": item_id}, update_data)

        if result.matched_count == 0:
            raise ValueError(f"Item with id {item_id} not found")

        updated_item = self.db[self.collection].find_one({"id": item_id})
        return Item(**updated_item)

    def delete_item(self, item_id: int) -> None:
        self.db[self.collection].delete_one({"id": item_id})