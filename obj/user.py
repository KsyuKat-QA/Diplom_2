import py_helper
import requests
import allure

class User:
    name = ''
    password = ''
    email = ''
    accessToken = ''

    BASE_URL = 'https://stellarburgers.nomoreparties.site/api/auth/'

    @allure.step('Задаем основные данные для пользоватея (логин, пароль, почта')
    def set_primary_data(self, data_3str):
        self.name, self.password, self.email = data_3str

    @allure.step('Если регистрация не прошла - затираем данные')
    def reset_primary_data(self):
        self.name, self.password, self.email = '','',''

    @allure.step('Генерируем основные данные (логин, почту, пароль) случайными строками')
    def gen_data_for_new_user(self):
        data = []
        for i in range(2):
            data.append(py_helper.generate_rnd_str_norm(10))  # генерим рандомные строки
        data.append(py_helper.generate_rnd_str_norm(10)+'@ya.ru') #делаем строку "почтой
        self.set_primary_data(data)

    @allure.step('Генерим нового юзера (из подготовленных данных) через вызов API')
    def gen_new_user(self):
        # собираем тело запроса
        payload = {
            "email": self.email,
            "password": self.password,
            "name": self.name
        }
        # отправляем запрос на регистрацию
        response = requests.post(self.BASE_URL+"register", json=payload)
        # если регистрация не прошла - сбрасываем данные
        if response.status_code != 200:
            self.reset_primary_data()
            return False
        else:
            return True

    @allure.step('Создаем нового юезра (цепочка генерации данных + вызов API)')
    def create_user(self):
        self.gen_data_for_new_user()
        return self.gen_new_user()

    @allure.step('Проверка, что юзер может залогиниться. В случае успеха - задаем ему токен')
    def try_login(self):
        payload = {
            "email": self.email,
            "password": self.password
        }
        response = requests.post(self.BASE_URL+"/login", data=payload)
        if response.status_code == 200:
            json_data = response.json()
            self.accessToken = json_data.get("accessToken")
            return True
        else:
            return False

    @allure.step('Проверка на изменение данных юзера')
    def try_change_user(self, new_mail, new_passwd, new_name):
        payload = {
            "email": new_mail,
            "password": new_passwd,
            "name": new_name
        }
        headers = {"Authorization": self.accessToken}
        response = requests.patch(self.BASE_URL+"/user", data=payload, headers=headers)
        if response.status_code == 200:
            return "OK"
        else:
            return response.text