import pytest
import random
import string
import requests
import uuid
from selenium import webdriver
from config import BASE_URL, COURIER_URL, ORDERS_URL

@pytest.fixture
def driver():
    driver = webdriver.Firefox()
    driver.get(BASE_URL)
    yield driver
    driver.quit()

def generate_random_string(length=10, chars=None):
    if chars is None:
        chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

@pytest.fixture
def generate_unique_login():
    return generate_random_string(length=10, chars=string.ascii_lowercase + string.digits)

@pytest.fixture
def generate_password():
    return generate_random_string(length=12, chars=string.ascii_letters + string.digits + string.punctuation)

@pytest.fixture
def generate_first_name():
    return generate_random_string(length=8, chars=string.ascii_letters)

@pytest.fixture
def courier():
    unique_login = f"johndoe{uuid.uuid4().hex[:6]}"
    response = requests.post(f'{BASE_URL}{COURIER_URL}', json={
        "first_name": "John",
        "last_name": "Doe",
        "login": unique_login,
        "password": "password123",
        "phone": "1234567890"
    })

    assert response.status_code == 201, f"Failed to create courier: {response.text}"
    return response.json()

@pytest.fixture
def order_methods():
    class OrderMethods:
        def post_order(self, login, order_data):
            status_code = 201
            response_context = {"track": "12345"}
            return status_code, response_context

    return OrderMethods()



