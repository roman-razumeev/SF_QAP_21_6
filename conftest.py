import requests
import pytest
import json
from settings import valid_email, valid_password
from settings import invalid_email, invalid_password
from settings import BASE_URL
from datetime import datetime
import sys


@pytest.fixture()
def get_key():

    headers = {
        'email': valid_email,
        'password': valid_password,
    }
    res = requests.get(BASE_URL+'api/key',
                             headers=headers)
    if 'key' not in res.json().keys():
        print('В запросе не передан ключ авторизации')

    try:
        result = res.json()
    except json.decoder.JSONDecodeError:
        result = res.text
    return result


@pytest.fixture(autouse=True)
def log_function(request):
    start_time = datetime.now()
    yield
    print('\n=========================================================')
    print(f'Test name: {request.function.__name__}')
    print(f'Start of test: {start_time}')
    print(request.module.__name__)
    print(request.fixturename)
    print(request.scope)
    print(request.cls)
    print(request.fspath)
    end_time = datetime.now()
    print ('==========================================================')
    print(f'End of test: {end_time}')
    print(f"Test duration: {end_time - start_time}")
    print ('==========================================================\n')


def log(func):
    """Декоратор, который логирует запросы в API тестах"""
    def wrapper_log(*args, **kwargs):
        # args_repr = [repr(a) for a in args]
        # # args_repr = [f"{a!r}" for a in args]
        # kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        # signature = ", ".join(args_repr + kwargs_repr)
        # print(f"Вызываем {func.__name__} параметры ({signature})")
        value = func(*args, **kwargs)
        # print(f"{func.__name__!r} вернула значение - {value!r}")
        print(value[2])
        # Записываем полученные ответы в файл log.txt:
        log_txt = "log_" + func.__name__ + ".txt"
        with open(log_txt, 'a', encoding='utf8') as my_file:
            my_file.write(f'Name Func: {func.__name__}\n'
                          f'Headers of query: {value[2]["Headers of query"]}\n'

                          f'Path parametrs: {value[2]["Path parametrs"]}\n'
                          f'Query parametrs: {value[2]["Query parametrs"]}\n'
                          f'Query body: {value[2]["Query body"]}\n'
                          f'Content: {value[2]["Content"]}\n'
                          f'Optional: {value[2]["Optional"]}\n'
                          f'URL: {value[2]["URL"]}\n'
                          f'Path URL: {value[2]["Path URL"]}\n'
                          f'Cookie: {value[2]["Cookie"]}\n'
                          f'==========================================================\n'
                          f'Response status: {value[0]}\n'
                          f'Response body:\n')
            json.dump(value[1], my_file, ensure_ascii=False, indent=4)

        return value[0], value[1]
    return wrapper_log

# @pytest.fixture(autouse=True)
# def request_fixture(request):
#     if 'Pets' in request.function.__name__:
#         print(f"\nЗапущен тест из сьюта Дом Питомца: {request.function.__name__}")

#
minversion = pytest.mark.skipif(
    sys.version_info < (3, 6), reason="at least mymodule-1.1 required"
)

# @pytest.fixture(autouse=True)
# def request_fixture(request):
#     print (f'Test name: {request.function.__name__}')
#     print (request.module.__name__)
#     print (request.fixturename)
#     print (request.scope)
#     print (request.cls)
#     print (request.fspath)




# def add_headers_tofile(*args, **kwargs):  # декоратор
#     def wrapper(request):  # функция обёртка
#         ## В двух нижних строках устанавливаем параметры запроса:
#         headers = {'email': valid_email, 'password': valid_password}
#         res = requests.get("https://petfriends.skillfactory.ru/api/key",
#                            headers=headers)
#         ##
#         content = res.headers  # обязательные заголовки
#         optional = res.request.headers  # опциональные заголовки
#         body = res.request.body  # тело запроса
#         cookie = res.cookies
#         url = res.request.url
#         # для вывода имени декорируемой функции в файле,
#         # используем аргумент обёртки - request:
#         name = request.node.name  # имя функции
#         status = res.status_code  # статус ответа
#         try:
#             result = res.json()  # тело ответа
#         except json.decoder.JSONDecodeError:
#             result = res.text
#         # Записываем полученные ответы в файл My_Headers:
#         with open("My_Headers.json", 'w', encoding='utf8') as my_file:
#             my_file.write(f'Name Func: {name}\nStatus: {status}\nContent: {content}\nOptional: {optional}\nRequest Body: '
#                           f'{body}\nCookies: {cookie}\nPath URL: {url}\n{res.request.path_url}\nResponse Body:\n')
#             json.dump(result, my_file, ensure_ascii=False, indent=4)
#         return status, result
#     return wrapper



