import pytest
from pydantic import ValidationError

from models.ingredient_model import Ingredient


def test_ingredient_creation():
    ingredient_data = {
        "name": "Sugar",
        "quantity": 100.0,
        "unit": "grams"
    }
    ingredient = Ingredient(**ingredient_data)
    assert ingredient.name == "Sugar"
    assert ingredient.quantity == 100.0
    assert ingredient.unit == "grams"


def test_ingredient_creation_with_defaults():
    ingredient_data = {
        "name": "Salt"
    }
    ingredient = Ingredient(**ingredient_data)
    assert ingredient.name == "Salt"
    assert ingredient.quantity is None
    assert ingredient.unit is None


def test_ingredient_validation_error():
    invalid_ingredient_data = {
        "name": "Sugar",
        "quantity": "100",
        "unit": "grams"
    }
    ingredient = Ingredient(**invalid_ingredient_data)
    assert ingredient.name == "Sugar"
    assert ingredient.quantity == 100.0
    assert ingredient.unit == "grams"


def test_ingredient_validation_error2():
    invalid_ingredient_data = {
        "name": "Sugar",
        "quantity": "100grams",
        "unit": ""
    }
    with pytest.raises(ValidationError) as excinfo:
        Ingredient(**invalid_ingredient_data)
    print(excinfo.value)


def test_ingredient_missing_fields():
    incomplete_ingredient_data = {
        "quantity": 100.0,
        "unit": "grams"
    }
    with pytest.raises(ValidationError) as excinfo:
        Ingredient(**incomplete_ingredient_data)
    print(excinfo.value)
