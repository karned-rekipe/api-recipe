import re
from typing import List
from urllib.parse import urlparse
from uuid import uuid4

from pymongo import MongoClient

from interfaces.item_interface import ItemRepository
from models.recipe_model import RecipeWrite
from schemas.item_schema import list_item_serial, item_serial

def check_uri(uri):
    if not re.match(r"^mongodb://", uri):
        raise ValueError("Invalid URI: URI must start with 'mongodb://'")


def extract_database(uri: str) -> str:
    parsed_uri = urlparse(uri)
    db_name = parsed_uri.path.lstrip("/")

    if not db_name:
        raise ValueError("L'URI MongoDB ne contient pas de nom de base de données.")

    return db_name


class ItemRepositoryMongo(ItemRepository):

    def __init__(self, uri):
        check_uri(uri)
        database = extract_database(uri)

        self.uri = uri
        self.client = MongoClient(self.uri)
        self.db = self.client[database]
        self.collection = "recipes"

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    #Todo
    # gerer l'erreur si insert_one ne fonctionne pas
    # du coup inserted_id n'existe pa
    def create_item(self, item_create: RecipeWrite) -> str:
        item_data = item_create.model_dump()
        item_data["_id"] = str(uuid4())
        new_uuid = self.db[self.collection].insert_one(item_data)
        return new_uuid.inserted_id

    def get_item(self, uuid: str) -> dict:
        result = self.db[self.collection].find_one({"_id": uuid})
        item = item_serial(result)
        return item

    def list_items(self) -> List[dict]:
        result = self.db[self.collection].find()
        items = list_item_serial(result)
        return items

    def update_item(self, uuid: str, item_update: RecipeWrite) -> None:
        update_data = {"$set": item_update.model_dump()}
        self.db[self.collection].find_one_and_update({"_id": uuid}, update_data)


    def delete_item(self, uuid: str) -> None:
        self.db[self.collection].delete_one({"_id": uuid})

    def close(self):
        self.client.close()
