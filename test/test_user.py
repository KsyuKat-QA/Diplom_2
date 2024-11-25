from obj.user import User
import requests
import pytest
import allure

@allure.title('Создание пользователя')
@allure.description('Проверяем создание экземпляра пользователя')
def test_user_create():
    tst_u = User()
    tst_u.gen_data_for_new_user()
    assert tst_u.gen_new_user()

@allure.title('Создание двух одинаковых юзеров')
@allure.description('Проверяем создание двух одинаковых юзеров. УСПЕХ = создан лишь один юзер')
def test_same_user_create():
    tst_u = User()
    tst_u.gen_data_for_new_user()
    tst_u2 = User()
    tst_u2.set_primary_data([tst_u.name,tst_u.password,tst_u.email])
    assert (tst_u.gen_new_user() and not tst_u2.gen_new_user())

@allure.title('Создание юзера (не все обяз. поля заданы)')
@allure.description('Проверяем создание юзера без пароля. УСПЕХ = юзер не создан')
def test_user_create_not_all_value():
    tst_u = User()
    tst_u.gen_data_for_new_user()
    payload = {
        "email": tst_u.email,
        "name": tst_u.name
    }
    response = requests.post(tst_u.BASE_URL+"register", data=payload)
    assert response.text == '{"success":false,"message":"Email, password and name are required fields"}'

@allure.title('Проверка логина')
@allure.description('Проверяем вход (имя, пароль) c корректными данным. УСПЕХ = логин')
def test_login_user():
    tst_u = User()
    tst_u.create_user()
    assert tst_u.try_login()

@allure.title('Проверка НЕлогина')
@allure.description('Проверяем вход (имя, пароль) c НЕкорректными данным. УСПЕХ != логин')
def test_bad_login_user():
    tst_u = User()
    tst_u.create_user()
    tst_u.password = tst_u.password+'x' #добавляем лишний символ
    assert not tst_u.try_login()

@allure.title('Проверка изменения данных')
@allure.description('Проверяем изменения данных после логина (3 разных кейса через параметризацию')
@pytest.mark.parametrize("add_mail,add_pdw,add_name",
                         [('_added_mail', '', ''),
                         ('', '_added_pwd', ''),
                          ('', '', '_added_name')])
def test_change_user(add_mail,add_pdw,add_name):
    tst_u = User()
    tst_u.create_user()
    tst_u.try_login()
    assert tst_u.try_change_user(tst_u.email+add_mail, tst_u.password+add_pdw, tst_u.name+add_name) == "OK"#передаем старые данные + новые

@allure.description('Проверяем НЕ изменения данных при плохом логине')
@pytest.mark.parametrize("add_mail,add_pdw,add_name",
                         [('_added_mail', '', ''),
                         ('', '_added_pwd', ''),
                          ('', '', '_added_name')])
def test_not_change_user(add_mail,add_pdw,add_name):
    tst_u = User()
    tst_u.create_user()
    tst_u.try_login()
    tst_u.accessToken = "" #затираем данные токена для авторизации
    assert tst_u.try_change_user(tst_u.email+add_mail, tst_u.password+add_pdw, tst_u.name+add_name) == '{"success":false,"message":"You should be authorised"}'