import os
from repositories.item_repository import ItemRepositoryMongo

API_TAG_NAME =  "Recipes"

ITEM_REPOSITORY = 'mongodb://localhost:27017'
ITEM_DB_NAME = "local"
ITEM_DB_COLLECTION = "items"

ITEM_REPO = ItemRepositoryMongo(url=ITEM_REPOSITORY, name=ITEM_DB_NAME, collection=ITEM_DB_COLLECTION)

# Configuration Keycloak
KEYCLOAK_URL = os.environ['KEYCLOAK_URL']
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
