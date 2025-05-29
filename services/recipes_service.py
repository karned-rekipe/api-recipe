from fastapi import HTTPException
from models.recipe_model import RecipeWrite

def create_recipe(new_recipe, repository) -> str:
    try:
        new_uuid = repository.create_recipe(new_recipe)
        if not isinstance(new_uuid, str):
            raise TypeError("The method create_recipe did not return a str.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while creating the recipe: {e}")

    return new_uuid

def get_recipes(repository) -> list[RecipeWrite]:
    try:
        recipes = repository.list_recipes()
        if not isinstance(recipes, list):
            raise TypeError("The method list_recipes did not return a list.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while get the list of recipes: {e}")

    return recipes


def get_recipe(uuid: str, repository) -> RecipeWrite:
    try:
        recipe = repository.get_recipe(uuid)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while get recipe: {e}")

    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return recipe

def update_recipe(uuid: str, recipe_update: RecipeWrite, repository) -> None:
    try:
        repository.update_recipe(uuid, recipe_update)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while updating the recipe: {e}")

def delete_recipe(uuid: str, repository) -> None:
    try:
        repository.delete_recipe(uuid)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while deleting the recipe: {e}")