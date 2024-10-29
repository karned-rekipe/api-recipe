from models.item_model import Item

def create_item(new_item, repository) -> str:
    new_item_id = repository.create_item(new_item)
    return new_item_id

def get_items(repository) -> list[Item]:
    return repository.list_items()

def get_item(item_id: str, repository) -> Item:
    item = repository.get_item(item_id)
    return item

def update_item(item_id: str, item_update: Item, repository) -> None:
    repository.update_item(item_id, item_update)

def delete_item(item_id: str, repository) -> None:
    repository.delete_item(item_id)
