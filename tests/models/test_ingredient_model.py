import pytest
from pydantic import ValidationError

from models.ingredient_model import Ingredient, BaseModel


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


def test_ingredient_quantity_none():
    """Test that None quantity is handled correctly by the validator."""
    ingredient_data = {
        "name": "Sugar",
        "quantity": None,
        "unit": "grams"
    }
    ingredient = Ingredient(**ingredient_data)
    assert ingredient.name == "Sugar"
    assert ingredient.quantity is None
    assert ingredient.unit == "grams"


def test_ingredient_quantity_string_conversion():
    """Test that a string quantity is converted to a float."""
    ingredient_data = {
        "name": "Sugar",
        "quantity": "123.45",
        "unit": "grams"
    }
    ingredient = Ingredient(**ingredient_data)
    assert ingredient.name == "Sugar"
    assert ingredient.quantity == 123.45
    assert ingredient.unit == "grams"


def test_ingredient_quantity_int_conversion():
    """Test that an int quantity is converted to a float."""
    ingredient_data = {
        "name": "Sugar",
        "quantity": 123,
        "unit": "grams"
    }
    ingredient = Ingredient(**ingredient_data)
    assert ingredient.name == "Sugar"
    assert ingredient.quantity == 123.0
    assert ingredient.unit == "grams"


def test_ingredient_quantity_invalid():
    """Test that an invalid quantity raises a ValidationError."""
    ingredient_data = {
        "name": "Sugar",
        "quantity": "not-a-number",
        "unit": "grams"
    }
    with pytest.raises(ValidationError) as excinfo:
        Ingredient(**ingredient_data)
    assert "Input should be a valid number" in str(excinfo.value)
