import inspect


def get_function_name():
    return inspect.currentframe().f_back.f_code.co_name
