import sys
import pytest
import requests
from api import PetFriends
from settings import BASE_URL
from settings import invalid_email, invalid_password
import os
from tests.conftest_probe import minversion

pf = PetFriends()


class TestClassPetFriends:

    def test_getAllPets(self, get_key):
        # print(get_key)
        headers = {'auth_key': get_key['key']}
        filter = {'filter': ''}
        # response = requests.get(url='https://petfriends.skillfactory.ru/api/pets',
        response = requests.get(BASE_URL + 'api/pets',
                                headers=headers, params=filter)
        assert response.status_code == 200, 'Запрос выполнен неуспешно'
        assert len(response.json().get('pets')) > 0, 'Количество питомцев не соответствует ожиданиям'

    def test_getMyPets(self, get_key):

        headers = {'auth_key': get_key['key']}
        filter = {'filter': 'my_pets'}
        response = requests.get(BASE_URL + 'api/pets',
                                headers=headers, params=filter)

        assert response.status_code == 200, 'Запрос выполнен неуспешно'
        assert response.headers.get('Content-Type') == 'application/json'  # 'text/html; charset=utf-8'
        assert len(response.json().get('pets')) > 0, 'Количество питомцев не соответствует ожиданиям'

# def test_request_1(request_fixture):
#     print (f'Прямо из теста - {request_fixture}')
#
class TestClassRequest:
    def test_request_2(self, request_fixture):
        print (f'Прямо из класса - {request_fixture}')

@pytest.mark.skip(reason="Баг в продукте - <ссылка>")
def test_one(): # Это наш тест, который находит тот самый баг
    pass

@pytest.mark.skipif(sys.version_info < (3, 6),
                    reason="Тест требует python версии 3.6 или выше")
def test_python36_and_greater():
    pass

# minversion = pytest.mark.skipif(
#     sys.version_info < (3, 6), reason="at least mymodule-1.1 required"
# )

@minversion
def test_python36_and_greater2():
    pass

@pytest.mark.xfail
def test_flaky():
    pass

# На платформе Windows ожидаем, что тест будет падать
@pytest.mark.xfail(sys.platform == "win32",
                   reason="Ошибка в системной библиотеке")
def test_not_for_windows():
    print(f'\n{sys.platform}')
    pass

@pytest.mark.xfail(raises=RuntimeError)
def test_x_status_runtime_only():
    pass


@pytest.mark.api
@pytest.mark.auth
def test_auth_api():
   pass

@pytest.mark.ui
@pytest.mark.auth
def test_auth_ui():
   pass

@pytest.mark.api
@pytest.mark.event
def test_event_api():
   pass

@pytest.mark.ui
@pytest.mark.event
def test_event_ui():
   pass


