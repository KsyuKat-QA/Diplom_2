from obj.order import Order
import pytest
import allure

@allure.title('Создание заказа без авторизации')
@allure.description('Проверяем создание заказа (генерим данные + вызов API) с разными комбинациями ингридиентов, в том числе без них и "кривыми"')
@pytest.mark.parametrize("ingdr_arr",
                         [
                            [0, 1],
                            [3, 4, 7],
                            [],  #пустые ингридиенты
                            [15], #кривой хэш
                         ])
def test_create_order_no_auth(ingdr_arr):
    ord = Order()
    if len(ingdr_arr)>0:
        if ingdr_arr[0]!=15: assert ord.create_order_no_auth(ingdr_arr) == 200
        else: assert ord.create_order_no_auth(ingdr_arr) == 500 #500 Internal Server Error для кривого хэша
    else: assert ord.create_order_no_auth(ingdr_arr) == 400 # Ingredient ids must be provided

@allure.title('Создание заказа с авторизацией')
@allure.description('Проверяем создание заказа (генерим данные + вызов API) с разными комбинациями ингридиентов. C авторизацией')
@pytest.mark.parametrize("ingdr_arr",
                         [
                            [0, 1],
                            [2]
                         ])
def test_create_order_auth(ingdr_arr):
    ord = Order()
    ord.create_user()
    ord.try_login()
    assert ord.create_order_auth(ingdr_arr)==200

@allure.title('Получаем списка заказов')
@allure.description('Получаем списка заказов сразу с двумя кейсами, с авторизацией (успех=200) и без нее (успех=401)')
@pytest.mark.parametrize("auth",
                         [
                            True,
                            False
                         ])
def test_get_orders_auth(auth):
    ord = Order()
    ord.create_user()
    if auth:
        ord.try_login()
        assert ord.get_orders()==200
    else:
        assert ord.get_orders()==401 #401 = You should be authorised
