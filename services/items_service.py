from fastapi import HTTPException
from models.item_model import Item

def create_item(new_item, repository) -> str:
    try:
        new_item_id = repository.create_item(new_item)
        if not isinstance(new_item_id, str):
            raise TypeError("The method create_item did not return a str.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while creating the item: {e}")

    return new_item_id

def get_items(repository) -> list[Item]:
    try:
        items = repository.list_items()
        if not isinstance(items, list):
            raise TypeError("The method list_items did not return a list.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while get the list of items: {e}")

    return items


def get_item(item_id: str, repository) -> Item:
    try:
        item = repository.get_item(item_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while get item: {e}")

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return item

def update_item(item_id: str, item_update: Item, repository) -> None:
    try:
        repository.update_item(item_id, item_update)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while updating the item: {e}")

def delete_item(item_id: str, repository) -> None:
    try:
        repository.delete_item(item_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while deleting the item: {e}")
