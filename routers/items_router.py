from fastapi import APIRouter, HTTPException, status, Request
from config.config import API_TAG_NAME
from decorators.check_permission import check_permissions
from models.item_model import Item
from services.items_service import create_item, get_items, get_item, update_item, delete_item


router = APIRouter(
    tags=[API_TAG_NAME]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
@check_permissions(['create'])
async def create_new_item(request: Request, item: Item) -> dict:
    repo = request.state.repo
    item.created_by = request.state.token_info.get('user_id')
    new_uuid = create_item(item, repo)
    return {"uuid": new_uuid}


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Item])
@check_permissions(['read', 'read_own'])
async def read_items(request: Request):
    repo = request.state.repo
    return get_items(repo)


@router.get("/{uuid}", status_code=status.HTTP_200_OK, response_model=Item)
@check_permissions(['list', 'list_own'])
async def read_item(request: Request, uuid: str):
    repo = request.state.repo
    item = get_item(uuid, repo)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
@check_permissions(['update', 'update_own'])
async def update_existing_item(request: Request, uuid: str, item_update: Item):
    repo = request.state.repo
    update_item(uuid, item_update, repo)


@router.delete("/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
@check_permissions(['delete', 'delete_own'])
async def delete_existing_item(request: Request, uuid: str):
    repo = request.state.repo
    delete_item(uuid, repo)

