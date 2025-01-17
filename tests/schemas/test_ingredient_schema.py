from schemas.ingredient_schema import list_ingredient_serial, ingredient_serial


def test_ingredient_serial():
    item = {
        "name": "Sugar",
        "quantity": 100,
        "unit": "grams"
    }
    expected_output = {
        "name": "Sugar",
        "quantity": 100,
        "unit": "grams"
    }
    assert ingredient_serial(item) == expected_output

    item_without_quantity_unit = {
        "name": "Salt"
    }
    expected_output_without_quantity_unit = {
        "name": "Salt",
        "quantity": None,
        "unit": None
    }
    assert ingredient_serial(item_without_quantity_unit) == expected_output_without_quantity_unit


def test_list_ingredient_serial():
    items = [
        {
            "name": "Sugar",
            "quantity": 100,
            "unit": "grams"
        },
        {
            "name": "Salt"
        }
    ]
    expected_output = [
        {
            "name": "Sugar",
            "quantity": 100,
            "unit": "grams"
        },
        {
            "name": "Salt",
            "quantity": None,
            "unit": None
        }
    ]
    assert list_ingredient_serial(items) == expected_output

    empty_items = []
    expected_output_empty = []
    assert list_ingredient_serial(empty_items) == expected_output_empty
