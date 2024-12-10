import pytest
from pydantic import ValidationError

from models.item_model import Item


def test_item_creation():
    item_data = {
        "name": "Recipe Name",
        "description": "This is a recipe description.",
        "price": 10.99,
        "quantity": 2,
        "number_of_persons": 4,
        "origin_country": "France",
        "attributes": ["vegan", "gluten-free"],
        "utensils": ["pan", "knife"],
        "ingredients": [
            {"name": "Sugar", "quantity": 100, "unit": "grams"},
            {"name": "Salt"}
        ],
        "steps": [
            {"step_number": 1, "description": "First step", "duration": "10 min"},
            {"step_number": 2, "description": "Second step"}
        ],
        "thumbnail_url": "http://example.com/thumbnail.jpg",
        "large_image_url": "http://example.com/large_image.jpg",
        "source_reference": "Source Reference"
    }
    item = Item(**item_data)
    assert item.name == "Recipe Name"
    assert item.description == "This is a recipe description."
    assert item.price == 10.99
    assert item.quantity == 2
    assert item.number_of_persons == 4
    assert item.origin_country == "France"
    assert item.attributes == ["vegan", "gluten-free"]
    assert item.utensils == ["pan", "knife"]
    assert len(item.ingredients) == 2
    assert len(item.steps) == 2
    assert str(item.thumbnail_url) == "http://example.com/thumbnail.jpg"
    assert str(item.large_image_url) == "http://example.com/large_image.jpg"
    assert item.source_reference == "Source Reference"


def test_item_creation_with_defaults():
    item_data = {
        "name": "Minimal Recipe"
    }
    item = Item(**item_data)
    assert item.name == "Minimal Recipe"
    assert item.description is None
    assert item.price is None
    assert item.quantity is None
    assert item.number_of_persons is None
    assert item.origin_country is None
    assert item.attributes == []
    assert item.utensils == []
    assert item.ingredients == []
    assert item.steps == []
    assert item.thumbnail_url is None
    assert item.large_image_url is None
    assert item.source_reference is None


def test_item_validation_error():
    invalid_item_data = {
        "name": "Invalid Recipe",
        "number_of_persons": 0
    }
    with pytest.raises(ValidationError):
        Item(**invalid_item_data)


def test_item_missing_fields():
    incomplete_item_data = {
        "description": "Incomplete Recipe"
    }
    with pytest.raises(ValidationError):
        Item(**incomplete_item_data)
