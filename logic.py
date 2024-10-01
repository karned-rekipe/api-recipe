from fastapi import HTTPException

def fetch_items():
    items = ["", "item1", "item2", "item3"]
    return items

def fetch_item(id_item: int):
    items = ["", "item1", "item2", "item3"]

    if id_item > len(items) - 1:
        raise HTTPException(status_code=404, detail='Item not found')
    
    return items[id_item]



