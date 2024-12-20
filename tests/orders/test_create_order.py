import pytest
import uuid
import allure
from tests.conftest import courier
from config import ORDER_DATA_1, ORDER_DATA_2, ORDER_DATA_3, ORDER_DATA_4

class TestCreateOrder:
    @pytest.mark.parametrize("order_data", [ORDER_DATA_1, ORDER_DATA_2, ORDER_DATA_3, ORDER_DATA_4])
    @allure.feature("Order Management")
    @allure.story("Create order")
    @allure.title("Test creating an order with various order data")
    def test_create_order(self, courier, order_methods, order_data):
        assert courier['ok'] is True

        login = f"johndoe{uuid.uuid4().hex[:6]}"
        status_code, response_context = order_methods.post_order(login, order_data)

        print(f"Status Code: {status_code}")
        print(f"Response: {response_context}")

        assert status_code == 201, f"Expected 201 but got {status_code}"
        assert 'track' in response_context, f"Expected 'track' in response but got {response_context}"

    @allure.feature("Order Management")
    @allure.story("Create order with both colors")
    @allure.title("Test creating an order with both colors")
    def test_order_with_both_colors(self, courier, order_methods):
        order_data = ORDER_DATA_3
        login = f"johndoe{uuid.uuid4().hex[:6]}"
        status_code, response_context = order_methods.post_order(login, order_data)

        print(f"Status Code: {status_code}")
        print(f"Response: {response_context}")

        assert status_code == 201, f"Expected 201 but got {status_code}"
        assert 'track' in response_context, f"Expected 'track' in response but got {response_context}"

    @allure.feature("Order Management")
    @allure.story("Create order without color")
    @allure.title("Test creating an order without specifying a color")
    def test_order_without_color(self, courier, order_methods):
        assert courier['ok'] is True

        order_data = ORDER_DATA_4
        login = f"johndoe{uuid.uuid4().hex[:6]}"
        status_code, response_context = order_methods.post_order(login, order_data)

        print(f"Status Code: {status_code}")
        print(f"Response: {response_context}")

        assert status_code == 201, f"Expected 201 but got {status_code}"
        assert 'track' in response_context, f"Expected 'track' in response but got {response_context}"
