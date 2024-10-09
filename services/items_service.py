from models.item import Item, ItemCreate

def create_item(new_item, repository) -> Item:
    repository.create_item(new_item)
    return new_item

def get_items(repository) -> list[Item]:
    return repository.list_items()

def get_item(item_id: int, repository) -> Item:
    Item = repository.get_item(item_id)
    return Item

def update_item(item_id: int, item_update: ItemCreate, repository) -> Item:
    repository.update_item(item_id, item_update)
    return Item

def delete_item(item_id: int, repository) -> bool:
    repository.delete_item(item_id)
    return False