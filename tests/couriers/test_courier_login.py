import pytest
import requests
import allure
from unittest.mock import patch
from methods.courier_methods import CourierMethods

@pytest.fixture
def courier_methods():
    return CourierMethods()

@allure.feature("Courier Login")
@allure.story("Login Success")
@allure.title("Test successful login")
def test_login_success(courier_methods):
    with patch("requests.post") as mock_post:
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response._content = b'{"token": "abcd1234"}'
        mock_post.return_value = mock_response

        response = courier_methods.login_courier("test_user", "test_password")

        assert response.get("token") == "abcd1234"
        assert "token" in response

@allure.feature("Courier Login")
@allure.story("Login Failure")
@allure.title("Test login failure due to incorrect credentials")
def test_login_failure(courier_methods):
    with patch("requests.post") as mock_post:
        mock_response = requests.Response()
        mock_response.status_code = 400
        mock_response._content = b'{"message": "Invalid credentials"}'
        mock_post.return_value = mock_response

        response = courier_methods.login_courier("wrong_user", "wrong_password")

        assert response.get("error") == "Invalid credentials"
        assert "error" in response


@allure.feature("Courier Login")
@allure.story("Login Failure")
@allure.title("Test login failure due to missing fields")
def test_login_missing_field(courier_methods):
    with patch("requests.post") as mock_post:
        mock_response = requests.Response()
        mock_response.status_code = 400
        mock_response._content = b'{"message": "Missing required field: login"}'
        mock_post.return_value = mock_response

        response = courier_methods.login_courier("", "test_password")

        assert response.get("error") == "Missing required field: login"

        mock_response._content = b'{"message": "Missing required field: password"}'
        mock_post.return_value = mock_response

        response = courier_methods.login_courier("test_user", "")

        assert response.get("error") == "Missing required field: password"

@allure.feature("Courier Login")
@allure.story("Login Failure")
@allure.title("Test login failure for non-existent user")
def test_login_non_existent_user(courier_methods):
    with patch("requests.post") as mock_post:
        mock_response = requests.Response()
        mock_response.status_code = 404
        mock_response._content = b'{"message": "User not found"}'
        mock_post.return_value = mock_response

        response = courier_methods.login_courier("non_existent_user", "test_password")

        assert response.get("error") == "User not found"
        assert "error" in response

@allure.feature("Courier Login")
@allure.story("Login Success")
@allure.title("Test successful login with ID")
def test_login_success_with_id(courier_methods):
    with patch("requests.post") as mock_post:
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response._content = b'{"token": "abcd1234", "id": 1}'
        mock_post.return_value = mock_response

        response = courier_methods.login_courier("test_user", "test_password")

        assert response.get("token") == "abcd1234"
        assert response.get("id") == 1
        assert "id" in response
        assert "token" in response


