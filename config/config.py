import os

from repositories.item_repository import ItemRepositoryMongo

API_NAME = "api-recipe"
API_TAG_NAME =  "Recipes"

ITEM_REPOSITORY = 'mongodb://localhost:27017'
ITEM_DB_NAME = "local"
ITEM_DB_COLLECTION = "recipes"

ITEM_REPO = ItemRepositoryMongo(url=ITEM_REPOSITORY, name=ITEM_DB_NAME, collection=ITEM_DB_COLLECTION)

KEYCLOAK_URL = os.environ['KEYCLOAK_URL']
