import requests, json

def log(func):
    """Выводит сигнатуру функции и возвращаемое значение"""
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
