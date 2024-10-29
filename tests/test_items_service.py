from fastapi.testclient import TestClient
from unittest import TestCase
from main import app

class TestAPI(TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_create_item(self):
        item_data = {
            "name": "Test Item",
            "description": "A simple test item",
            "price": 10.99,
            "quantity": 5
        }

        response = self.client.post("/", json=item_data)

        self.assertEqual(response.status_code, 201)

        response_data = response.json()