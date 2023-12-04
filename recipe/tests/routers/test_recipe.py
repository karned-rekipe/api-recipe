import pytest
import requests

from recipe.config import api_v, api

API_BASE_URL = "http://127.0.0.1:8001/v" + api_v + "/" + api

ulid_test = ''


def test_post_recipe():
    global ulid_test
    recipe_data = {
        "label": "Label test"
    }
    response = requests.post(f"{API_BASE_URL}/", json = recipe_data)
    assert response.status_code == 201
    updated_recipe_data = response.json()

    # maj de la variable globale ulid_test
    ulid_test = updated_recipe_data["_id"]


def test_get_recipe():
    response = requests.get(f"{API_BASE_URL}/")
    assert response.status_code == 200
    # recipe_data = response.json()
    # assert recipe_data["name"] == "John Doe"


def test_get_recipe_by_ulid():
    global ulid_test
    response = requests.get(f"{API_BASE_URL}/" + ulid_test + "/")
    assert response.status_code == 200
    recipe_data = response.json()
    assert recipe_data["label"] == "Label test"


def test_get_recipe_by_ulid_wrong():
    response = requests.get(f"{API_BASE_URL}/TOTO/")
    assert response.status_code == 404


def test_patch_recipe():
    recipe_data = {
        "label": "Label new"
    }
    response = requests.patch(f"{API_BASE_URL}/" + ulid_test + "/", json = recipe_data)
    assert response.status_code == 204

    response = requests.get(f"{API_BASE_URL}/" + ulid_test + "/")
    assert response.status_code == 200
    recipe_data = response.json()
    assert recipe_data["label"] == "Label new"


def test_delete_recipe():
    global ulid_test
    response = requests.delete(f"{API_BASE_URL}/" + ulid_test + "/")
    assert response.status_code == 202

    response = requests.get(f"{API_BASE_URL}/" + ulid_test + "/")
    assert response.status_code == 404

if __name__ == "__main__":
    pytest.main()
