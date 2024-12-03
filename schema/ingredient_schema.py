def ingredient_serial(ing) -> dict:
    return {
        "name": ing["name"],
        "quantity": ing.get("quantity"),
        "unit": ing.get("unit")
    }