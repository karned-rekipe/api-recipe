def ingredient_serial(item) -> dict:
    return {
        "name": item["name"],
        "quantity": item.get("quantity"),
        "unit": item.get("unit"),
        "created_by": item.get("created_by")
    }


def list_ingredient_serial(items) -> list:
    return [ingredient_serial(item) for item in items]
