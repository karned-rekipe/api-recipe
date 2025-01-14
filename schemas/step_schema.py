def step_serial(item) -> dict:
    return {
        "step_number": item["step_number"],
        "description": item["description"],
        "duration": item.get("duration")
    }


def list_step_serial(items) -> list:
    return [step_serial(item) for item in items]
