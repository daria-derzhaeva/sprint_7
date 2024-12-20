import pytest
import uuid
import allure
from methods.courier_methods import CourierMethods

class TestCourier:
    @allure.feature("Courier Creation")
    @allure.story("Create Courier")
    @allure.title("Test successful courier creation")
    def test_create_courier(self, generate_unique_login, generate_password, generate_first_name):
        login = generate_unique_login
        password = generate_password
        first_name = generate_first_name

        courier_data = CourierMethods().create_courier(login, password, first_name)
        assert courier_data.get('ok') is True, "Courier creation failed"

    @allure.feature("Courier Creation")
    @allure.story("Create Courier with Missing Field")
    @allure.title("Test courier creation with missing field")
    @pytest.mark.parametrize("missing_field, request_data", [
        ("login", {"password": "lfy3748", "first_name": "TestName"}),
        ("password", {"login": f"test_{uuid.uuid4().hex[:8]}", "first_name": "TestName"}),
    ])
    def test_missing_field(self, missing_field, request_data):
        request_data.pop(missing_field, None)

        response = CourierMethods().create_courier(**request_data)
        print(f"Response: {response}")

        assert response.get("ok") is None, f"Expected error but got success response: {response}"

        assert response.get("message") == "Недостаточно данных для создания учетной записи", \
            f"Unexpected message: {response.get('message')}"

    @allure.feature("Courier Creation")
    @allure.story("Create Courier with Existing Login")
    @allure.title("Test courier creation with existing login")
    @pytest.mark.parametrize("existing_login, request_data", [
        ("existing_login", {"login": "existing_login", "password": "lfy3748", "first_name": "TestName"})
    ])
    def test_create_user_with_existing_login(self, existing_login, request_data):
        CourierMethods().create_courier(**request_data)

        response = CourierMethods().create_courier(**request_data)

        print(f"Response: {response}")

        assert response.get("code") == 409, f"Expected code 409 but got {response.get('code')}. Response: {response}"
        assert response.get("message") == "Этот логин уже используется. Попробуйте другой.", \
            f"Unexpected message: {response.get('message')}"
