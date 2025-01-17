import os
import redis
from repositories.item_repository import ItemRepositoryMongo

API_NAME = os.environ['API_NAME']
API_TAG_NAME = os.environ['API_TAG_NAME']

ITEM_REPOSITORY = 'mongodb://localhost:27017'
ITEM_DB_NAME = "local"
ITEM_DB_COLLECTION = "recipes"
ITEM_REPO = ItemRepositoryMongo(url=ITEM_REPOSITORY, name=ITEM_DB_NAME, collection=ITEM_DB_COLLECTION)

KEYCLOAK_HOST = os.environ['KEYCLOAK_HOST']
KEYCLOAK_REALM = os.environ['KEYCLOAK_REALM']

REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = int(os.environ['REDIS_PORT'])
REDIS_DB = int(os.environ['REDIS_DB'])
REDIS_PASSWORD = os.environ['REDIS_PASSWORD']