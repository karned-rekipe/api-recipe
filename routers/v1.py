from fastapi import APIRouter, HTTPException, status, Request
from config.config import API_TAG_NAME
from common_api.decorators.v0.check_permission import check_permissions
from models.recipe_model import RecipeWrite, RecipeRead
from common_api.services.v0 import Logger
from services.recipes_service import create_recipe, get_recipes, get_recipe, update_recipe, delete_recipe

logger = Logger()

VERSION = "v1"
api_group_name = f"/{API_TAG_NAME}/{VERSION}/"

router = APIRouter(
    tags=[api_group_name],
    prefix=f"/recipe/{VERSION}"
)


@router.post("/", status_code=status.HTTP_201_CREATED)
@check_permissions(['create'])
async def create_new_recipe(request: Request, recipe: RecipeWrite) -> dict:
    logger.api("POST /recipe/v1/")
    recipe.created_by = request.state.token_info.get('user_uuid')
    new_uuid = create_recipe(request, recipe)
    return {"uuid": new_uuid}


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[RecipeRead])
@check_permissions(['read', 'read_own'])
async def read_recipes(request: Request):
    logger.api("GET /recipe/v1/")
    return get_recipes(request)


@router.get("/{uuid}", status_code=status.HTTP_200_OK, response_model=RecipeRead)
@check_permissions(['list', 'list_own'])
async def read_recipe(request: Request, uuid: str):
    logger.api("GET /recipe/v1/{uuid}")
    recipe = get_recipe(request, uuid)
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.put("/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
@check_permissions(['update', 'update_own'])
async def update_existing_recipe(request: Request, uuid: str, recipe_update: RecipeWrite):
    logger.api("PUT /recipe/v1/{uuid}")
    update_recipe(request, uuid, recipe_update)


@router.delete("/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
@check_permissions(['delete', 'delete_own'])
async def delete_existing_recipe(request: Request, uuid: str):
    logger.api("DELETE /recipe/v1/{uuid}")
    delete_recipe(request, uuid)
