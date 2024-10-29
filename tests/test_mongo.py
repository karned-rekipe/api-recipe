from unittest import TestCase
from pymongo import MongoClient
from models.item_model import ItemCreate
from repositories.item_repository import ItemRepositoryMongo

class TestMongoDB(TestCase):

    def setUp(self):
        self.mongo_url = "mongodb://localhost:27017"
        self.mongo_db_name = "test_db"
        self.mongo_collection_name = "test_items"
        self.repository = ItemRepositoryMongo(self.mongo_url, self.mongo_db_name, self.mongo_collection_name)

        with self.repository as repo:
            repo.db[self.mongo_collection_name].delete_many({})

    def test_populate_mongodb(self):
        item_create = ItemCreate(name="Test Item", description="A simple test item", price=10.99, quantity=5)

        with self.repository as repo:
            repo.create_item(item_create)

            inserted_item = repo.db[self.mongo_collection_name].find_one({"name": "Test Item"})
            self.assertIsNotNone(inserted_item)
            self.assertEqual(inserted_item['name'], "Test Item")
            self.assertEqual(inserted_item['price'], 10.99)