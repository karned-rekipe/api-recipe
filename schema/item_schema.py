from schema.ingredient_schema import ingredient_serial
from schema.step_schema import step_serial


def individual_serial(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "description": item.get("description"),
        "price": item.get("price"),
        "quantity": item.get("quantity"),
        "number_of_persons": item.get("number_of_persons"),
        "origin_country": item.get("origin_country"),
        "attributes": item.get("attributes", []),
        "utensils": item.get("utensils", []),
        "ingredients": [ingredient_serial(ing) for ing in item.get("ingredients", [])],
        "steps": [step_serial(step) for step in item.get("steps", [])],
        "thumbnail_url": item.get("thumbnail_url"),
        "large_image_url": item.get("large_image_url"),
        "source_reference": item.get("source_reference")
    }

def list_serial(items) -> list:
    return[individual_serial(item) for item in items]


