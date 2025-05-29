import pytest
from pydantic import ValidationError

from models.recipe_model import RecipeWrite


def test_recipe_creation():
    recipe_data = {
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
    recipe = RecipeWrite(**recipe_data)
    assert recipe.name == "Recipe Name"
    assert recipe.description == "This is a recipe description."
    assert recipe.price == 10.99
    assert recipe.quantity == 2
    assert recipe.number_of_persons == 4
    assert recipe.origin_country == "France"
    assert recipe.attributes == ["vegan", "gluten-free"]
    assert recipe.utensils == ["pan", "knife"]
    assert len(recipe.ingredients) == 2
    assert len(recipe.steps) == 2
    assert str(recipe.thumbnail_url) == "http://example.com/thumbnail.jpg"
    assert str(recipe.large_image_url) == "http://example.com/large_image.jpg"
    assert recipe.source_reference == "Source Reference"


def test_recipe_creation_with_defaults():
    recipe_data = {
        "name": "Minimal Recipe"
    }
    recipe = RecipeWrite(**recipe_data)
    assert recipe.name == "Minimal Recipe"
    assert recipe.description is None
    assert recipe.price is None
    assert recipe.quantity is None
    assert recipe.number_of_persons is None
    assert recipe.origin_country is None
    assert recipe.attributes == []
    assert recipe.utensils == []
    assert recipe.ingredients == []
    assert recipe.steps == []
    assert recipe.thumbnail_url is None
    assert recipe.large_image_url is None
    assert recipe.source_reference is None


def test_recipe_validation_error():
    invalid_recipe_data = {
        "name": "Invalid Recipe",
        "number_of_persons": 0
    }
    with pytest.raises(ValidationError):
        RecipeWrite(**invalid_recipe_data)


def test_recipe_missing_fields():
    incomplete_recipe_data = {
        "description": "Incomplete Recipe"
    }
    with pytest.raises(ValidationError):
        RecipeWrite(**incomplete_recipe_data)

def test_recipe_invalid_description_type():
    invalid_recipe_data = {
        "name": "Invalid Recipe",
        "description": 123
    }
    with pytest.raises(ValidationError):
        RecipeWrite(**invalid_recipe_data)

def test_recipe_invalid_price_type():
    invalid_recipe_data = {
        "name": "Invalid Recipe",
        "price": "ten"
    }
    with pytest.raises(ValidationError):
        RecipeWrite(**invalid_recipe_data)

def test_recipe_invalid_quantity_type():
    invalid_recipe_data = {
        "name": "Invalid Recipe",
        "quantity": "two"
    }
    with pytest.raises(ValidationError):
        RecipeWrite(**invalid_recipe_data)

def test_recipe_invalid_number_of_persons_type():
    invalid_recipe_data = {
        "name": "Invalid Recipe",
        "number_of_persons": "four"
    }
    with pytest.raises(ValidationError):
        RecipeWrite(**invalid_recipe_data)

def test_recipe_invalid_origin_country_type():
    invalid_recipe_data = {
        "name": "Invalid Recipe",
        "origin_country": 42
    }
    with pytest.raises(ValidationError):
        RecipeWrite(**invalid_recipe_data)

def test_recipe_invalid_attributes_type():
    invalid_recipe_data = {
        "name": "Invalid Recipe",
        "attributes": "vegan"
    }
    with pytest.raises(ValidationError):
        RecipeWrite(**invalid_recipe_data)

def test_recipe_invalid_utensils_type():
    invalid_recipe_data = {
        "name": "Invalid Recipe",
        "utensils": "pan"
    }
    with pytest.raises(ValidationError):
        RecipeWrite(**invalid_recipe_data)

def test_recipe_invalid_ingredients_type():
    invalid_recipe_data = {
        "name": "Invalid Recipe",
        "ingredients": "Sugar"
    }
    with pytest.raises(ValidationError):
        RecipeWrite(**invalid_recipe_data)

def test_recipe_invalid_steps_type():
    invalid_recipe_data = {
        "name": "Invalid Recipe",
        "steps": "First step"
    }
    with pytest.raises(ValidationError):
        RecipeWrite(**invalid_recipe_data)

def test_recipe_invalid_thumbnail_url_type():
    invalid_recipe_data = {
        "name": "Invalid Recipe",
        "thumbnail_url": 123
    }
    with pytest.raises(ValidationError):
        RecipeWrite(**invalid_recipe_data)

def test_recipe_invalid_large_image_url_type():
    invalid_recipe_data = {
        "name": "Invalid Recipe",
        "large_image_url": 123
    }
    with pytest.raises(ValidationError):
        RecipeWrite(**invalid_recipe_data)

def test_recipe_invalid_source_reference_type():
    invalid_recipe_data = {
        "name": "Invalid Recipe",
        "source_reference": 123
    }
    with pytest.raises(ValidationError):
        RecipeWrite(**invalid_recipe_data)

def test_recipe_invalid_url():
    invalid_recipe_data = {
        "name": "Invalid Recipe",
        "thumbnail_url": "invalid_url",
        "large_image_url": "invalid_url"
    }
    with pytest.raises(ValidationError):
        RecipeWrite(**invalid_recipe_data)

def test_recipe_invalid_list_types():
    invalid_recipe_data = {
        "name": "Invalid Recipe",
        "attributes": ["vegan", 123],
        "utensils": ["pan", 42]
    }
    with pytest.raises(ValidationError):
        RecipeWrite(**invalid_recipe_data)