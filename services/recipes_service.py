from fastapi import HTTPException
from models.recipe_model import RecipeWrite
from common_api.utils.v0 import get_state_repos


def create_recipe(request, new_recipe) -> str:
    try:
        repos = get_state_repos(request)
        new_uuid = repos.recipe_repo.create_recipe(new_recipe)
        if not isinstance(new_uuid, str):
            raise TypeError("The method create_recipe did not return a str.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while creating the recipe: {e}")

    return new_uuid

def get_recipes(request) -> list[RecipeWrite]:
    try:
        repos = get_state_repos(request)
        recipes = repos.recipe_repo.list_recipes()
        if not isinstance(recipes, list):
            raise TypeError("The method list_recipes did not return a list.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while get the list of recipes: {e}")

    return recipes


def get_recipe(request, uuid: str) -> RecipeWrite:
    try:
        repos = get_state_repos(request)
        recipe = repos.recipe_repo.get_recipe(uuid)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while retrieving the recipe: {e}")

    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return recipe

def update_recipe(request, uuid: str, recipe_update: RecipeWrite) -> None:
    try:
        repos = get_state_repos(request)
        repos.recipe_repo.update_recipe(uuid, recipe_update)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while updating the recipe: {e}")

def delete_recipe(request, uuid: str) -> None:
    try:
        repos = get_state_repos(request)
        repos.recipe_repo.delete_recipe(uuid)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while deleting the recipe: {e}")