import os
from datetime import datetime

def logger(old_function):
    def new_function(*args, **kwargs):
        date = datetime.now().strftime('%d-%m-%Y  %H:%M:%S')
        name = old_function.__name__
        result = old_function(*args, **kwargs)
        with open('main.txt', 'a', encoding='utf-8') as f:
            f.write(f''' {date},
{name},
{result},
{args, kwargs}\n''')
        return result

    return new_function


def logger_path(path):

    def __logger(old_function):
        def new_function(*args, **kwargs):
            date = datetime.now().strftime('%d-%m-%Y  %H:%M:%S')
            name = old_function.__name__
            result = old_function(*args, **kwargs)
            with open(path, 'a', encoding='utf-8') as f:
                f.write(f''' {date},
{name},
{result},
{args, kwargs}\n''')
            return result

        return new_function
    return __logger
