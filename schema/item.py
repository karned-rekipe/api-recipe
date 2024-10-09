def individual_serial(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "description": item["description"],
        "price": item["price"],
        "quantity": item["quantity"]
    }

def list_serial(items) -> list:
    return[individual_serial(item) for item in items]


