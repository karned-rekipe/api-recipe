from typing import List

from pymongo import MongoClient
from models.item_model import Item, ItemCreate
from interfaces.item_interface import ItemRepository
from uuid import uuid4

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

    #Todo
    # gerer l'erreur si insert_one ne fonctionne pas
    # du coup inserted_id n'existe pa
    def create_item(self, item_create: Item) -> str:
        item_data = item_create.model_dump()
        item_data["_id"] = str(uuid4())
        new_item_id = self.db[self.collection].insert_one(item_data)
        return new_item_id.inserted_id

    def get_item(self, item_id: int) -> Item:
        data = self.db[self.collection].find_one({"id": item_id})
        return Item(**data) if data else None

    def list_items(self) -> List[ItemCreate]:
        items = self.db[self.collection].find()
        return [ItemCreate(**item) for item in items]

    def update_item(self, item_id: int, item_update: Item) -> ItemCreate:
        update_data = {"$set": item_update.model_dump()}
        result = self.db[self.collection].update_one({"id": item_id}, update_data)

        if result.matched_count == 0:
            raise ValueError(f"Item with id {item_id} not found")

        updated_item = self.db[self.collection].find_one({"id": item_id})
        return ItemCreate(**updated_item)

    def delete_item(self, item_id: int) -> None:
        self.db[self.collection].delete_one({"id": item_id})