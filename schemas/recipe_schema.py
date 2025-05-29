from schemas.ingredient_schema import list_ingredient_serial
from schemas.step_schema import list_step_serial


def recipe_serial(recipe) -> dict:
    return {
        "uuid": str(recipe["_id"]),
        "name": recipe["name"],
        "description": recipe.get("description"),
        "price": recipe.get("price"),
        "quantity": recipe.get("quantity"),
        "number_of_persons": recipe.get("number_of_persons"),
        "origin_country": recipe.get("origin_country"),
        "attributes": recipe.get("attributes", []),
        "utensils": recipe.get("utensils", []),
        "ingredients": list_ingredient_serial(recipe.get("ingredients", [])),
        "steps": list_step_serial(recipe.get("steps", [])),
        "thumbnail_url": recipe.get("thumbnail_url"),
        "large_image_url": recipe.get("large_image_url"),
        "source_reference": recipe.get("source_reference"),
        "created_by": recipe.get("created_by")
    }


def list_recipe_serial(recipes) -> list:
    return [recipe_serial(recipe) for recipe in recipes]