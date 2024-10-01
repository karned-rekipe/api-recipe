from models.item import Item, ItemCreate

# Simulation d'une base de données en mémoire
fake_items_db = [
    Item(id=1, name="Item 1", description="First item", price=10.5, quantity=100),
    Item(id=2, name="Item 2", description="Second item", price=15.0, quantity=50)
]

# Fonction pour créer un item
def create_item(item_create: ItemCreate) -> Item:
    new_id = len(fake_items_db) + 1
    new_item = Item(id=new_id, **item_create.dict())
    fake_items_db.append(new_item)
    return new_item

# Fonction pour récupérer tous les items
def get_items() -> list[Item]:
    return fake_items_db

# Fonction pour récupérer un item par ID
def get_item(item_id: int) -> Item:
    for item in fake_items_db:
        if item.id == item_id:
            return item
    return None

# Fonction pour mettre à jour un item
def update_item(item_id: int, item_update: ItemCreate) -> Item:
    for index, item in enumerate(fake_items_db):
        if item.id == item_id:
            updated_item = Item(id=item_id, **item_update.dict())
            fake_items_db[index] = updated_item
            return updated_item
    return None

# Fonction pour supprimer un item
def delete_item(item_id: int) -> bool:
    for index, item in enumerate(fake_items_db):
        if item.id == item_id:
            del fake_items_db[index]
            return True
    return False