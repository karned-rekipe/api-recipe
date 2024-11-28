def individual_serial(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"],  # Obligatoire
        "description": item.get("description"),  # Optionnel
        "price": item.get("price"),  # Optionnel
        "quantity": item.get("quantity"),  # Optionnel
        "number_of_persons": item.get("number_of_persons"),  # Optionnel
        "origin_country": item.get("origin_country"),  # Optionnel
        "attributes": item.get("attributes", []),  # Optionnel, liste par défaut
        "utensils": item.get("utensils", []),  # Optionnel, liste par défaut
        "ingredients": [
            {
                "name": ing["name"],
                "quantity": ing.get("quantity"),  # Optionnel
                "unit": ing.get("unit")  # Optionnel
            } for ing in item.get("ingredients", [])
        ],
        "steps": [
            {
                "step_number": step["step_number"],
                "description": step["description"],
                "duration": step.get("duration")  # Optionnel
            } for step in item.get("steps", [])
        ],
        "thumbnail_url": item.get("thumbnail_url"),  # Optionnel
        "large_image_url": item.get("large_image_url"),  # Optionnel
        "source_reference": item.get("source_reference")  # Optionnel
    }

def list_serial(items) -> list:
    return[individual_serial(item) for item in items]


