import requests
from config import BASE_URL, ORDERS_URL

class OrderMethods:
    def post_order(self, id, params):
        response = requests.post(f'{BASE_URL}{ORDERS_URL}', json=params)
        return response.status_code, response.json()

    def delete_order(self, id, params):
        response = requests.delete(f'{BASE_URL}{ORDERS_URL}delete/{id}', json=params)
        return response.status_code, response.json()

