from models.item_model import Item, ItemCreate

def create_item(new_item, repository) -> None:
    print(new_item)
    repository.create_item(new_item)

def get_items(repository) -> list[Item]:
    return repository.list_items()

def get_item(item_id: int, repository) -> Item:
    item = repository.get_item(item_id)
    return item

def update_item(item_id: int, item_update: ItemCreate, repository) -> None:
    repository.update_item(item_id, item_update)

def delete_item(item_id: int, repository) -> None:
    repository.delete_item(item_id)
