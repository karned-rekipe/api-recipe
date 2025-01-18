import logging
from repositories.item_repository import ItemRepositoryMongo

def get_db(uuid) -> ItemRepositoryMongo:
    logging.info(f"Config : get_db: {uuid}")
    if uuid == "d3f48a42-0d1e-4270-8e8e-549251cd823d":
        host = 'localhost'
        port = 27017
        url = f"mongodb://{host}:{port}"
        db = "local"
        collection = "recipes"
        return ItemRepositoryMongo(url=url, name=db, collection=collection)