from schemas.recipe_schema import recipe_serial, list_recipe_serial


def test_recipe_serial_with_difficulty():
    recipe = {
        "created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d",
        "_id": "12345",
        "name": "Recipe with Difficulty",
        "description": "This recipe has a difficulty level.",
        "price": 15.50,
        "difficulty": 4,
        "quantity": 1,
        "number_of_persons": 2,
        "origin_country": "Italy"
    }
    expected_output = {
        "created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d",
        "uuid": "12345",
        "name": "Recipe with Difficulty",
        "description": "This recipe has a difficulty level.",
        "price": 15.50,
        "difficulty": 4,
        "quantity": 1,
        "number_of_persons": 2,
        "origin_country": "Italy",
        "attributes": [],
        "utensils": [],
        "ingredients": [],
        "steps": [],
        "thumbnail_url": None,
        "large_image_url": None,
        "source_reference": None
    }
    assert recipe_serial(recipe) == expected_output


def test_recipe_serial():
    recipe = {
        "created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d",
        "_id": "12345",
        "name": "Recipe Name",
        "description": "This is a recipe description.",
        "price": 10.99,
        "quantity": 2,
        "number_of_persons": 4,
        "origin_country": "France",
        "attributes": ["vegan", "gluten-free"],
        "utensils": ["pan", "knife"],
        "ingredients": [
            {"created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d", "name": "Sugar", "quantity": 100, "unit": "grams"},
            {"created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d", "name": "Salt"}
        ],
        "steps": [
            {"created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d", "step_number": 1, "description": "First step", "duration": 10},
            {"created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d", "step_number": 2, "description": "Second step"}
        ],
        "thumbnail_url": "http://example.com/thumbnail.jpg",
        "large_image_url": "http://example.com/large_image.jpg",
        "source_reference": "Source Reference"
    }
    expected_output = {
        "created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d",
        "uuid": "12345",
        "name": "Recipe Name",
        "description": "This is a recipe description.",
        "price": 10.99,
        "difficulty": None,
        "quantity": 2,
        "number_of_persons": 4,
        "origin_country": "France",
        "attributes": ["vegan", "gluten-free"],
        "utensils": ["pan", "knife"],
        "ingredients": [
            {"created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d", "name": "Sugar", "quantity": 100, "unit": "grams"},
            {"created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d", "name": "Salt", "quantity": None, "unit": None}
        ],
        "steps": [
            {"created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d", "step_number": 1, "description": "First step", "duration": 10},
            {"created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d", "step_number": 2, "description": "Second step", "duration": None}
        ],
        "thumbnail_url": "http://example.com/thumbnail.jpg",
        "large_image_url": "http://example.com/large_image.jpg",
        "source_reference": "Source Reference"
    }
    assert recipe_serial(recipe) == expected_output

    recipe_minimal = {
        "created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d",
        "_id": "67890",
        "name": "Minimal Recipe"
    }
    expected_output_minimal = {
        "created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d",
        "uuid": "67890",
        "name": "Minimal Recipe",
        "description": None,
        "price": None,
        "difficulty": None,
        "quantity": None,
        "number_of_persons": None,
        "origin_country": None,
        "attributes": [],
        "utensils": [],
        "ingredients": [],
        "steps": [],
        "thumbnail_url": None,
        "large_image_url": None,
        "source_reference": None
    }
    assert recipe_serial(recipe_minimal) == expected_output_minimal


def test_list_recipe_serial():
    recipes = [
        {
            "created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d",
            "_id": "12345",
            "name": "Recipe Name",
            "description": "This is a recipe description.",
            "price": 10.99,
            "quantity": 2,
            "number_of_persons": 4,
            "origin_country": "France",
            "attributes": ["vegan", "gluten-free"],
            "utensils": ["pan", "knife"],
            "ingredients": [
                {"created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d", "name": "Sugar", "quantity": 100, "unit": "grams"},
                {"created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d", "name": "Salt"}
            ],
            "steps": [
                {"created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d", "step_number": 1, "description": "First step", "duration": 10},
                {"created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d", "step_number": 2, "description": "Second step"}
            ],
            "thumbnail_url": "http://example.com/thumbnail.jpg",
            "large_image_url": "http://example.com/large_image.jpg",
            "source_reference": "Source Reference"
        },
        {
            "created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d",
            "_id": "67890",
            "name": "Minimal Recipe"
        }
    ]
    expected_output = [
        {
            "created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d",
            "uuid": "12345",
            "name": "Recipe Name",
            "description": "This is a recipe description.",
            "price": 10.99,
            "difficulty": None,
            "quantity": 2,
            "number_of_persons": 4,
            "origin_country": "France",
            "attributes": ["vegan", "gluten-free"],
            "utensils": ["pan", "knife"],
            "ingredients": [
                {"created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d", "name": "Sugar", "quantity": 100, "unit": "grams"},
                {"created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d", "name": "Salt", "quantity": None, "unit": None}
            ],
            "steps": [
                {"created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d", "step_number": 1, "description": "First step", "duration": 10},
                {"created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d", "step_number": 2, "description": "Second step", "duration": None}
            ],
            "thumbnail_url": "http://example.com/thumbnail.jpg",
            "large_image_url": "http://example.com/large_image.jpg",
            "source_reference": "Source Reference"
        },
        {
            "created_by": "d3f48a42-0d1e-4270-8e8e-549251cd823d",
            "uuid": "67890",
            "name": "Minimal Recipe",
            "description": None,
            "price": None,
            "difficulty": None,
            "quantity": None,
            "number_of_persons": None,
            "origin_country": None,
            "attributes": [],
            "utensils": [],
            "ingredients": [],
            "steps": [],
            "thumbnail_url": None,
            "large_image_url": None,
            "source_reference": None
        }
    ]
    assert list_recipe_serial(recipes) == expected_output

    empty_recipes = []
    expected_output_empty = []
    assert list_recipe_serial(empty_recipes) == expected_output_empty