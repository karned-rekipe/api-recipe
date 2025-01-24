from schemas.ingredient_schema import list_ingredient_serial, ingredient_serial


def test_ingredient_serial():
    item = {
        "created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d",
        "name": "Sugar",
        "quantity": 100,
        "unit": "grams"
    }
    expected_output = {
        "created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d",
        "name": "Sugar",
        "quantity": 100,
        "unit": "grams"
    }
    assert ingredient_serial(item) == expected_output

    item_without_quantity_unit = {
        "created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d",
        "name": "Salt"
    }
    expected_output_without_quantity_unit = {
        "created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d",
        "name": "Salt",
        "quantity": None,
        "unit": None
    }
    assert ingredient_serial(item_without_quantity_unit) == expected_output_without_quantity_unit


def test_list_ingredient_serial():
    items = [
        {
            "created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d",
            "name": "Sugar",
            "quantity": 100,
            "unit": "grams"
        },
        {
            "created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d",
            "name": "Salt"
        }
    ]
    expected_output = [
        {
            "created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d",
            "name": "Sugar",
            "quantity": 100,
            "unit": "grams"
        },
        {
            "created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d",
            "name": "Salt",
            "quantity": None,
            "unit": None
        }
    ]
    assert list_ingredient_serial(items) == expected_output

    empty_items = []
    expected_output_empty = []
    assert list_ingredient_serial(empty_items) == expected_output_empty
