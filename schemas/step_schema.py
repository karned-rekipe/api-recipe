def step_serial(item) -> dict:
    return {
        "step_number": item.get("step_number"),
        "title": item.get("title"),
        "description": item.get("description"),
        "duration": item.get("duration"),
        "created_by": item.get("created_by"),
        "cooking_time": item.get("cooking_time"),
        "rest_duration": item.get("rest_duration"),
        "preparation_time": item.get("preparation_time")
    }


def list_step_serial(items) -> list:
    return [step_serial(item) for item in items]
