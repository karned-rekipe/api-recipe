from fastapi import APIRouter, HTTPException, status
from config.config import API_TAG_NAME
from models.item import Item, ItemCreate
from services.items_service import create_item, get_items, get_item, update_item, delete_item
from config.config import ITEM_REPOSITORY

router = APIRouter(
    tags=[API_TAG_NAME]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_new_item(item_create: ItemCreate):
    new_item = create_item(item_create, ITEM_REPOSITORY)
    return new_item

@router.get("/", response_model=list[Item], status_code=status.HTTP_200_OK)
async def read_items():
    return get_items(ITEM_REPOSITORY)

@router.get("/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
async def read_item(item_id: int):
    item = get_item(item_id, ITEM_REPOSITORY)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_existing_item(item_id: int, item_update: ItemCreate):
    updated_item = update_item(item_id, item_update, ITEM_REPOSITORY)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_item(item_id: int):
    success = delete_item(item_id, ITEM_REPOSITORY)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}