import logging
import os

from pymongo import MongoClient
from pymongo.database import Database
from icecream import ic
from pymongo.server_api import ServerApi

from recipe.config import *


class Mongodb:
    client: MongoClient = None
    db: Database = None

    def connect_to_database(self):
        uri = "mongodb://172.17.0.2:27017/"

        current_dir = os.path.dirname(os.path.abspath(__file__))
        pem_path = os.path.join(current_dir, '../../env', 'recipe.pem')

        logging.info("Connecting to MongoDB.")
        self.client = MongoClient(uri)
        self.db = self.client[mongo_database]
        logging.info("Connected to MongoDB.")

    def close_database_connection(self):
        logging.info("Closing connection with MongoDB.")
        self.client.close()
        logging.info("Closed connection with MongoDB.")

    def list(self, collection_name: str, query: dict):
        collection = self.db[collection_name]
        documents = collection.find(query)
        response = [doc for doc in documents]
        return response

    def create(self, collection_name: str, insert):
        collection = self.db[collection_name]
        if 'id' in insert:
            insert['_id'] = insert.pop('id')

        collection.insert_one(insert)
        return {'_id': insert['_id']}

    def read(self, collection_name: str, query: dict):
        collection = self.db[collection_name]
        response = collection.find_one(query)
        return response

    def update(self, collection_name: str, filter: dict, update: dict):
        collection = self.db[collection_name]
        collection.find_one_and_update(filter, update)
        response = collection.find_one({'_id': filter['_id']})
        return response

    def delete(self, collection_name: str, filter: dict):
        collection = self.db[collection_name]
        response = collection.find_one_and_delete(filter)
        return response


mongodb = Mongodb()
