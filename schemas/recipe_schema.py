from schemas.process_schema import list_process_serial


def recipe_serial(recipe) -> dict:
    return {
        "uuid": str(recipe["_id"]),
        "name": recipe["name"],
        "description": recipe.get("description"),
        "price": recipe.get("price"),
        "difficulty": recipe.get("difficulty"),
        "quantity": recipe.get("quantity"),
        "number_of_persons": recipe.get("number_of_persons"),
        "origin_country": recipe.get("origin_country"),
        "attributes": recipe.get("attributes", []),
        "process": list_process_serial(recipe.get("process", [])),
        "thumbnail_url": recipe.get("thumbnail_url"),
        "large_image_url": recipe.get("large_image_url"),
        "source_reference": recipe.get("source_reference"),
        "created_by": recipe.get("created_by")
    }


def list_recipe_serial(recipes) -> list:
    return [recipe_serial(recipe) for recipe in recipes]