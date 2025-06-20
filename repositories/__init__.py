from common_api.services.v0 import Logger
from repositories.recipe_repository_mongo import RecipeRepositoryMongo

logger = Logger()

class Repositories:
    def __init__(self, recipe_repo=None):
        self.recipe_repo = recipe_repo

def get_repositories(uri):
    if uri.startswith("mongodb"):
        logger.info("Using MongoDB repositories")
        return Repositories(
            recipe_repo=RecipeRepositoryMongo(uri)
        )

    return Repositories
