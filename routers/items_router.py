from contextlib import contextmanager
from fastapi import APIRouter, HTTPException, status, Depends
from config.config import API_TAG_NAME
from models.item_model import Item, ItemCreate
from services.items_service import create_item, get_items, get_item, update_item, delete_item
from config.config import ITEM_REPO


def get_repo():
    with ITEM_REPO as repo:
        yield repo


router = APIRouter(
    tags=[API_TAG_NAME]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_new_item(item: Item, repo=Depends(get_repo)) -> dict:
    new_item_id = create_item(item, repo)
    print(new_item_id)
    return {"uuid": new_item_id}

@router.get("/", response_model=list[ItemCreate], status_code=status.HTTP_200_OK)
async def read_items(repo=Depends(get_repo)):
    return get_items(repo)


@router.get("/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
async def read_item(item_id: int, repo=Depends(get_repo)):
    item = get_item(item_id, repo)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_existing_item(item_id: int, item_update: ItemCreate, repo=Depends(get_repo)):
    update_item(item_id, item_update, repo)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_item(item_id: int, repo=Depends(get_repo)):
    delete_item(item_id, repo)

