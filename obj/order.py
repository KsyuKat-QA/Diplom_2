import allure
from obj.user import User
import requests

class Order(User):
    ingdr_avaliable = [
        "61c0c5a71d1f82001bdaaa6d",
        "61c0c5a71d1f82001bdaaa6f",
        "61c0c5a71d1f82001bdaaa70",
        "61c0c5a71d1f82001bdaaa71",
        "61c0c5a71d1f82001bdaaa72",
        "61c0c5a71d1f82001bdaaa6e",
        "61c0c5a71d1f82001bdaaa73",
        "61c0c5a71d1f82001bdaaa74",
        "61c0c5a71d1f82001bdaaa6c",
        "61c0c5a71d1f82001bdaaa75",
        "61c0c5a71d1f82001bdaaa76",
        "61c0c5a71d1f82001bdaaa77",
        "61c0c5a71d1f82001bdaaa78",
        "61c0c5a71d1f82001bdaaa79",
        "61c0c5a71d1f82001bdaaa7a",
        "xxx"
    ]
    ingdr_list = []

    BASE_URL_ORDER = 'https://stellarburgers.nomoreparties.site/api/orders'

    @allure.step('Задаем ингридиенты из доступных для дальнейшего формирования запроса')
    def fill_ingdr_list(self, ingdr_arr):
        for i in ingdr_arr:
            self.ingdr_list.append(self.ingdr_avaliable[i])

    @allure.step('Создаем заказ без авторизации)')
    def create_order_no_auth(self, ingdr_arr):
        if len(ingdr_arr)>0:
            self.fill_ingdr_list(ingdr_arr)
            payload = {
                "ingredients": self.ingdr_list
            }
        else: payload = {}
        response = requests.post(self.BASE_URL_ORDER, data=payload)
        return response.status_code

    @allure.step('Создаем заказ с авторизацией)')
    def create_order_auth(self, ingdr_arr):
        if len(ingdr_arr)>0:
            self.fill_ingdr_list(ingdr_arr)
            payload = {
                "ingredients": self.ingdr_list
            }
        else: payload = {}
        headers = {"Authorization": self.accessToken}
        response = requests.post(self.BASE_URL_ORDER, data=payload, headers=headers)
        return response.status_code

    @allure.step('Получаем список заказов')
    def get_orders(self):
        headers = {"Authorization": self.accessToken}
        response = requests.get(self.BASE_URL_ORDER, headers=headers)
        return response.status_code
