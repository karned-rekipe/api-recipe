from fastapi import APIRouter, HTTPException, status
from config import API_TAG_NAME
from models.item import Item, ItemCreate
from services.items_service import create_item, get_items, get_item, update_item, delete_item

router = APIRouter(
    tags=[API_TAG_NAME]
)

# CREATE: Créer un nouvel item
@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_new_item(item_create: ItemCreate):
    new_item = create_item(item_create)
    return new_item

# READ: Récupérer tous les items
@router.get("/", response_model=list[Item], status_code=status.HTTP_200_OK)
async def read_items():
    return get_items()

# READ: Récupérer un item par ID
@router.get("/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
async def read_item(item_id: int):
    item = get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# UPDATE: Mettre à jour un item par ID
@router.put("/{item_id}", response_model=Item, status_code=status.HTTP_204_NO_CONTENT)
async def update_existing_item(item_id: int, item_update: ItemCreate):
    updated_item = update_item(item_id, item_update)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

# DELETE: Supprimer un item par ID
@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_item(item_id: int):
    success = delete_item(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}