def step_serial(step) -> dict:
    return {
        "step_number": step["step_number"],
        "description": step["description"],
        "duration": step.get("duration")
    }