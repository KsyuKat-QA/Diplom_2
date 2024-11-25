py_helper.py - генерация случайных данных

obj:
	user.py - описание класса "пользователь". Описывает поля и методы работы с ними
	order.py - описание класса "заказ". Описывает ингридиенты и методы работы c заказом

test:
	test_user.py 
		def test_user_create - Создание пользователя
		def test_same_user_create - Создание двух одинаковых юзеров
		def test_user_create_not_all_value - Создание юзера (не все обяз. поля заданы)
		def test_login_user - Проверка логина
		def test_bad_login_user - Проверка НЕлогина
		def test_change_user - Проверка изменения данных
		def test_not_change_user - Проверяем НЕ изменения данных при плохом логине
	test_order.py
		def test_create_order_no_auth - Создание заказа без авторизации с разными комбинациями ингридиентов, в том числе без них и "кривыми"
		def test_create_order_auth - Создание заказа с авторизацией
		def test_get_orders_auth - Получаем список заказов с авторизацией и без