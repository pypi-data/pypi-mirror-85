""" Switch example for python 3 """


def _say_hello() -> str:
    return 'Hello'


def _say_goodbye() -> str:
    return 'Good bye'


def _unknown_salute() -> str:
    return 'Unknown salute :('


# Cases are outside the "switch" method in order to create them just once
_CASES = {0: _say_hello, 1: _say_goodbye}


def switch(case: int) -> str:
    """
    Switch like method
    :param case: Case
    :return: Case evaluation
    """
    return _CASES.get(case, _unknown_salute)()


if __name__ == '__main__':
    print(f'{switch(0)}, {switch(1)}, {switch(2)}')
