import re
from typing import List
from urllib.parse import urlparse
from uuid import uuid4

from pymongo import MongoClient

from interfaces.recipe_interface import RecipeRepository
from models.recipe_model import RecipeWrite
from schemas.recipe_schema import list_recipe_serial, recipe_serial

def check_uri(uri):
    if not re.match(r"^mongodb://", uri):
        raise ValueError("Invalid URI: URI must start with 'mongodb://'")


def extract_database(uri: str) -> str:
    parsed_uri = urlparse(uri)
    db_name = parsed_uri.path.lstrip("/")

    if not db_name:
        raise ValueError("L'URI MongoDB ne contient pas de nom de base de données.")

    return db_name


class RecipeRepositoryMongo(RecipeRepository):

    def __init__(self, uri):
        check_uri(uri)
        database = extract_database(uri)

        self.uri = uri
        self.client = MongoClient(self.uri)
        self.db = self.client[database]
        self.collection = "recipes"

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def create_recipe(self, recipe_create: RecipeWrite) -> str:
        recipe_data = recipe_create.model_dump()
        recipe_id = str(uuid4())
        recipe_data["_id"] = recipe_id
        try:
            new_uuid = self.db[self.collection].insert_one(recipe_data)
            return new_uuid.inserted_id
        except Exception as e:
            raise ValueError(f"Failed to create recipe in database: {str(e)}")

    def get_recipe(self, uuid: str) -> dict:
        result = self.db[self.collection].find_one({"_id": uuid})
        if result is None:
            return None
        recipe = recipe_serial(result)
        return recipe

    def list_recipes(self) -> List[dict]:
        result = self.db[self.collection].find()
        recipes = list_recipe_serial(result)
        return recipes

    def update_recipe(self, uuid: str, recipe_update: RecipeWrite) -> None:
        update_fields = recipe_update.model_dump()
        update_fields.pop('created_by', None)
        update_data = {"$set": update_fields}
        self.db[self.collection].find_one_and_update({"_id": uuid}, update_data)


    def delete_recipe(self, uuid: str) -> None:
        self.db[self.collection].delete_one({"_id": uuid})

    def close(self):
        self.client.close()
