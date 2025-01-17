from schemas.step_schema import step_serial, list_step_serial


def test_step_serial():
    item = {
        "created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d",
        "step_number": 1,
        "description": "First step",
        "duration": 10
    }
    expected_output = {
        "created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d",
        "step_number": 1,
        "description": "First step",
        "duration": 10
    }
    assert step_serial(item) == expected_output

    item_without_duration = {
        "created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d",
        "step_number": 2,
        "description": "Second step"
    }
    expected_output_without_duration = {
        "created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d",
        "step_number": 2,
        "description": "Second step",
        "duration": None
    }
    assert step_serial(item_without_duration) == expected_output_without_duration


def test_list_step_serial():
    items = [
        {
            "created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d",
            "step_number": 1,
            "description": "First step",
            "duration": 10
        },
        {
            "created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d",
            "step_number": 2,
            "description": "Second step"
        }
    ]
    expected_output = [
        {
            "created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d",
            "step_number": 1,
            "description": "First step",
            "duration": 10
        },
        {
            "created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d",
            "step_number": 2,
            "description": "Second step",
            "duration": None
        }
    ]
    assert list_step_serial(items) == expected_output

    empty_items = []
    expected_output_empty = []
    assert list_step_serial(empty_items) == expected_output_empty
