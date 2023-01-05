import requests, pytest, json
from settings import valid_email, valid_password
from settings import invalid_email, invalid_password
from settings import BASE_URL
from datetime import datetime
import sys


minversion = pytest.mark.skipif(
    sys.version_info < (3, 6), reason="at least mymodule-1.1 required"
)

@pytest.fixture()
def request_fixture(request):
    print(request.fixturename)
    print(request.scope)
    print(request.function.__name__)
    print(request.cls)
    print(request.module.__name__)
    print(request.fspath)
    if request.cls:
        return f"\n У теста {request.function.__name__} класс есть\n"
    else:
        return f"\n У теста {request.function.__name__} класса нет\n"

@pytest.fixture(autouse=True)
def request_fixture(request):
    if 'Pets' in request.function.__name__:
        print(f"\nЗапущен тест из сьюта Дом Питомца: {request.function.__name__}")


@pytest.fixture(scope='class')
def get_key():
    headers = {
        'email': valid_email,
        'password': valid_password,
    }
    res = requests.get(BASE_URL+'api/key',
                             headers=headers)

    assert res.status_code == 200, 'Запрос выполнен неуспешно'
    assert 'key' in res.json().keys(), 'В запросе не передан ключ авторизации'
    try:
        result = res.json()
    except json.decoder.JSONDecodeError:
        result = res.text
    return result


@pytest.fixture(autouse=True)
def time_delta():
    start_time = datetime.now()
    yield
    end_time = datetime.now()
    print (f"\nТест шел: {end_time - start_time}")


@pytest.fixture
def some_data():
    return 42