import logging
from repositories.item_repository import ItemRepositoryMongo

def get_db(uuid) -> ItemRepositoryMongo:
    logging.info(f"Config : get_db: {uuid}")
    if uuid == 'd3f48a42-0d1e-4270-8e8e-549251cd823d':
        uri = f"mongodb://localhost:27017/local"
        return ItemRepositoryMongo(uri=uri)