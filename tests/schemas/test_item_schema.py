from schemas.item_schema import item_serial, list_item_serial


def test_item_serial():
    item = {
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
            {"name": "Sugar", "quantity": 100, "unit": "grams"},
            {"name": "Salt"}
        ],
        "steps": [
            {"step_number": 1, "description": "First step", "duration": 10},
            {"step_number": 2, "description": "Second step"}
        ],
        "thumbnail_url": "http://example.com/thumbnail.jpg",
        "large_image_url": "http://example.com/large_image.jpg",
        "source_reference": "Source Reference"
    }
    expected_output = {
        "id": "12345",
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
            {"name": "Salt", "quantity": None, "unit": None}
        ],
        "steps": [
            {"step_number": 1, "description": "First step", "duration": 10},
            {"step_number": 2, "description": "Second step", "duration": None}
        ],
        "thumbnail_url": "http://example.com/thumbnail.jpg",
        "large_image_url": "http://example.com/large_image.jpg",
        "source_reference": "Source Reference"
    }
    assert item_serial(item) == expected_output

    item_minimal = {
        "_id": "67890",
        "name": "Minimal Recipe"
    }
    expected_output_minimal = {
        "id": "67890",
        "name": "Minimal Recipe",
        "description": None,
        "price": None,
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
    assert item_serial(item_minimal) == expected_output_minimal


def test_list_item_serial():
    items = [
        {
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
                {"name": "Sugar", "quantity": 100, "unit": "grams"},
                {"name": "Salt"}
            ],
            "steps": [
                {"step_number": 1, "description": "First step", "duration": 10},
                {"step_number": 2, "description": "Second step"}
            ],
            "thumbnail_url": "http://example.com/thumbnail.jpg",
            "large_image_url": "http://example.com/large_image.jpg",
            "source_reference": "Source Reference"
        },
        {
            "_id": "67890",
            "name": "Minimal Recipe"
        }
    ]
    expected_output = [
        {
            "id": "12345",
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
                {"name": "Salt", "quantity": None, "unit": None}
            ],
            "steps": [
                {"step_number": 1, "description": "First step", "duration": 10},
                {"step_number": 2, "description": "Second step", "duration": None}
            ],
            "thumbnail_url": "http://example.com/thumbnail.jpg",
            "large_image_url": "http://example.com/large_image.jpg",
            "source_reference": "Source Reference"
        },
        {
            "id": "67890",
            "name": "Minimal Recipe",
            "description": None,
            "price": None,
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
    assert list_item_serial(items) == expected_output

    empty_items = []
    expected_output_empty = []
    assert list_item_serial(empty_items) == expected_output_empty
