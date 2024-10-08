from repositories.item import ItemRepositoryMongo

API_TAG_NAME =  "Recipes"

ITEM_REPOSITORY = 'mongodb://localhost:27017'
ITEM_DB_NAME = "local"

ITEM_REPOSITORY = ItemRepositoryMongo(url=ITEM_REPOSITORY, name=ITEM_DB_NAME)