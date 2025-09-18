from schemas.ingredient_schema import list_ingredient_serial
from schemas.step_schema import list_step_serial


def process_serial(item) -> dict:
    return {
        "name": item.get("name"),
        "recipe_uuid": item.get("recipe_uuid"),
        "utensils": item.get("utensils", []),
        "ingredients": list_ingredient_serial(item.get("ingredients", [])),
        "steps": list_step_serial(item.get("steps", []))
    }

def list_process_serial(items) -> list:
    return [process_serial(item) for item in items]