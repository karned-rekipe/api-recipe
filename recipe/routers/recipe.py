from typing import List

from fastapi import APIRouter, status, Query, Body
from icecream import ic
from recipe.config import *
from recipe.schemas.recipe import (SchemaRecipeCreate, SchemaRecipeId, SchemaRecipeRead,
                                   SchemaRecipeUpdate, ModelRecipeComputeFields)
from recipe.functions.recipe import *

router = APIRouter()
collection = 'recipe'


@router.get("/healthchecker/",
            name = "Simple healthcheck",
            summary = "Simple healthcheck",
            description = "Simple healthcheck",
            response_description = "Confirmation message",
            responses = responses_healthcheck,
            status_code = status.HTTP_200_OK)
async def healthcheck():
    """ Healthcheck
    """
    message = 'API /v' + api_v + '/' + api + ' is LIVE!'
    return {"message": message}


@router.get("/",
            summary = "List recipe",
            description = "Return a list of recipes",
            response_description = "List of recipe",
            responses = responses_default,
            response_model = list[SchemaRecipeRead],
            status_code = status.HTTP_200_OK)
async def list_recipe(
        _id: str = Query(None, description = "Optional id query"),
        label: str = Query(None, description = "Optional name query")
) -> list[Recipe]:
    """ Get a list of recipes
    """
    recipes = get_all(_id, label)
    return recipes


@router.post("/",
             summary = "Create recipe",
             description = "Create a new recipe",
             response_description = "UILD of the created recipe",
             responses = responses_default,
             response_model = SchemaRecipeId,
             status_code = status.HTTP_201_CREATED)
async def post_recipe(payload: SchemaRecipeCreate = Body(...)) -> SchemaRecipeId:
    """ Create a new recipe
    """
    recipe_id = create(ModelRecipe(**payload.model_dump()))
    return recipe_id


@router.get("/{_id}",
            summary = "Read recipe",
            description = "Get recipe by ulid",
            response_description = "Recipe",
            responses = responses_default,
            response_model = SchemaRecipeRead)
async def get_recipe(_id: str) -> Recipe:
    """ Get information about a recipe
    """
    recipe = get_by_id(_id)
    return recipe


@router.patch("/{_id}",
              summary = "Update recipe",
              description = "Update recipe",
              response_description = "status code",
              responses = responses_update,
              status_code = status.HTTP_204_NO_CONTENT)
async def update_recipe(_id: str, payload: SchemaRecipeUpdate = Body(...)) -> None:
    """ Update a recipe
    """
    update(payload.model_dump(), _id)
    return None


@router.delete("/{_id}",
               summary = "Delete recipe",
               description = "Delete recipe by ulid",
               response_description = "status code",
               responses = responses_delete,
               status_code = status.HTTP_202_ACCEPTED)
async def delete_recipe(_id: str) -> None:
    """ Delete a recipe
    """
    delete(_id)
    return None
