import pytest
import requests
import allure
from config import BASE_URL, COURIER_URL, ORDERS_URL
from helpers import generate_random_login
from faker import Faker

fake = Faker()

class TestOrders:
    @pytest.mark.parametrize("password, first_name, order_data, expected_status_code", [
        ("1234", "saske", {
            "firstName": fake.first_name(),
            "lastName": fake.last_name(),
            "address": f"{fake.city()}, {fake.building_number()} {fake.street_name()}",
            "metroStation": fake.random_int(min=1, max=10),
            "phone": fake.phone_number(),
            "rentTime": fake.random_int(min=1, max=10),
            "deliveryDate": fake.date(),
            "comment": fake.sentence(),
            "color": ["BLACK"]
        }, 200)
    ])
    @allure.feature("Order Management")
    @allure.story("Create order and get list")
    @allure.title("Test creating an order and getting the order list")
    def test_create_order_and_get_list(self, password, first_name, order_data, expected_status_code):
        login = generate_random_login()
        courier_data = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        print(f"Creating courier with data: {courier_data}")
        response_create_courier = requests.post(f"{BASE_URL}{COURIER_URL}", json=courier_data)
        print(f"Create courier response: {response_create_courier.status_code} - {response_create_courier.text}")
        assert response_create_courier.status_code == 201, f"Failed to create courier: {response_create_courier.text}"

        print(f"Creating order with data: {order_data}")
        response_create_order = requests.post(f"{BASE_URL}{ORDERS_URL}", json=order_data)
        print(f"Create order response: {response_create_order.status_code} - {response_create_order.text}")
        assert response_create_order.status_code == 201, f"Failed to create order: {response_create_order.text}"
        order_id = response_create_order.json().get("track")
        assert order_id, "Order track was not returned"

        login_data = {
            "login": login,
            "password": password
        }
        print(f"Logging in with data: {login_data}")
        response_login_courier = requests.post(f"{BASE_URL}{COURIER_URL}/login", json=login_data)
        print(f"Login response: {response_login_courier.status_code} - {response_login_courier.text}")
        assert response_login_courier.status_code == 200, f"Failed to login courier: {response_login_courier.text}"

        courier_id = response_login_courier.json().get("id")
        assert courier_id, "Courier ID was not returned after login"
        print(f"Courier ID after login: {courier_id}")

        response_accept_order = requests.put(f"{BASE_URL}{ORDERS_URL}/accept/{order_id}?courierId={courier_id}")
        assert response_accept_order.status_code == 200, f"Failed to accept order: {response_accept_order.text}"

        url = f"{BASE_URL}{ORDERS_URL}?courierId={courier_id}"
        response_get_orders = requests.get(url)
        assert response_get_orders.status_code == expected_status_code, f"Expected {expected_status_code} but got {response_get_orders.status_code}"
        response_json = response_get_orders.json()
        assert "orders" in response_json, f"Expected 'orders' in response but got {response_json}"

        orders = response_json.get("orders", [])
        assert len(orders) > 0, f"No orders found for courier {courier_id}"
        assert any(order["id"] == order_id for order in orders), f"Order {order_id} not found for courier {courier_id}"
