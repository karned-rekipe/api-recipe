from fastapi import APIRouter, HTTPException, status, Depends, Request
from config.config import API_TAG_NAME
from decorators.check_permission import check_permissions
from models.item_model import Item
from services.items_service import create_item, get_items, get_item, update_item, delete_item
from config.config import ITEM_REPO
from services.auth_service import  verif_token


def get_repo():
    with ITEM_REPO as repo:
        yield repo



router = APIRouter(
    tags=[API_TAG_NAME],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
@check_permissions(['create'])
async def create_new_item(item: Item, repo=Depends(get_repo)) -> dict:
    new_item_id = create_item(item, repo)
    return {"uuid": new_item_id}

@router.get("/", status_code=status.HTTP_200_OK, dependencies=[Depends(verif_token)])
#@check_permissions(['read', 'read_own'])
async def read_items(request: Request, repo=Depends(get_repo)):
    return get_items(repo)


@router.get("/{item_id}", status_code=status.HTTP_200_OK)
@check_permissions(['list', 'list_own'])
async def read_item(item_id: str, repo=Depends(get_repo)):
    item = get_item(item_id, repo)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
@check_permissions(['update', 'update_own'])
async def update_existing_item(item_id: str, item_update: Item, repo=Depends(get_repo)):
    update_item(item_id, item_update, repo)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
@check_permissions(['delete', 'delete_own'])
async def delete_existing_item(item_id: str, repo=Depends(get_repo)):
    delete_item(item_id, repo)

