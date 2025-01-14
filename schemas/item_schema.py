from schemas.ingredient_schema import list_ingredient_serial
from schemas.step_schema import list_step_serial


def item_serial(item) -> dict:
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
        "ingredients": list_ingredient_serial(item.get("ingredients", [])),
        "steps": list_step_serial(item.get("steps", [])),
        "thumbnail_url": item.get("thumbnail_url"),
        "large_image_url": item.get("large_image_url"),
        "source_reference": item.get("source_reference"),
        "created_by": item.get("created_by"),
    }


def list_item_serial(items) -> list:
    return [item_serial(item) for item in items]
