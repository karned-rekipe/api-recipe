def step_serial(item) -> dict:
    return {
        "step_number": item["step_number"],
        "title": item["title"],
        "description": item["description"],
        "duration": item.get("duration"),
        "created_by": item.get("created_by"),
        "cooking_time": item.get("cooking_time"),
        "rest_duration": item.get("rest_duration"),
        "preparation_time": item.get("preparation_time")
    }


def list_step_serial(items) -> list:
    return [step_serial(item) for item in items]
