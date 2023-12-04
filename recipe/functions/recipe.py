import re

from fastapi import HTTPException, status

from recipe.db import mongodb
from recipe.models import ModelRecipe
from recipe.entities import Recipe


def get_all(_id: str, label: str) -> list[Recipe]:
    query = {}
    if _id:
        query['_id'] = {"$regex": f'.*{re.escape(_id)}.*'}

    if label:
        query['label'] = {"$regex": f'.*{re.escape(label)}.*'}

    recipes_data = mongodb.list(Recipe.DB_CONTAINER, query)

    if recipes_data is None:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = {
                "message": "An error occurred while get list of recipes",
                "doc": "http://127.0.0.1:8000/v5/recipe/docs#/Recipe/Recipes_list_v5_recipe__get"
            })

    recipes = [Recipe(ModelRecipe(**recipe_data)) for recipe_data in recipes_data]

    return recipes


def get_by_id(_id: str) -> Recipe:
    recipe = mongodb.read(Recipe.DB_CONTAINER, {"_id": _id})

    if recipe is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = {
                "message": f"Recipe '{_id}' not found",
                "doc": "http://127.0.0.1:8000/v5/recipe/docs#/Recipe/Get_a_recipe_v5_recipe__id__get"
            })

    recipe_resp = Recipe(ModelRecipe(**recipe))

    return recipe_resp


def create(payload: ModelRecipe):
    recipe_id = mongodb.create(Recipe.DB_CONTAINER, payload.model_dump())

    if recipe_id is None:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = {
                "message": "Sorry, something happen during the recipe creation"
            }
        )

    return recipe_id


def update(payload: dict, _id: str):
    get_by_id(_id)

    recipe_update = mongodb.update(Recipe.DB_CONTAINER, {"_id": _id}, {"$set": payload})

    if recipe_update is None:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = {
                "message": "Sorry, something happen during the recipe update"
            }
        )

    return None


def delete(_id: str):
    get_by_id(_id)

    mongodb.delete(Recipe.DB_CONTAINER, {"_id": _id})
    return None
