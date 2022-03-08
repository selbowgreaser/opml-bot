import re
import math
from typing import Optional
import sympy as sp
from sympy import symbols, sympify
from numpy import inf

from .operations_name_gen import allowed_operations, forbidden_names_for_variables


def check_variables(variables: str, split_by: Optional[str] = None) -> str:
    """
    Функция для проверки переменных на корректность имени.
     
    На вход принимает строку с переменными, после проверки возвращает отдельно /
    первую и вторую переменные.

    Parameters:
    ------------
    variables: str
        Строка содержащая имена переменных.
    split_by: Optional[str] = None
        Разделитель переменных в строке. По умолчанию работает как обычный.

    Returns:
    -------
    str
        Строка с переменными, которые разделены пробелом.
    """

    if len(variables.split(split_by)) != 2:
        raise ValueError('Введенное количество переменных не равно двум')
    else:
        x, y = variables.split(split_by)
        correct_name_filter = re.compile(f'^[a-zA-Z]+[0-9]?$')

        if correct_name_filter.match(x) and correct_name_filter.match(y):
            for name in forbidden_names_for_variables:

                if x.find(name) != -1:
                    raise ValueError('Первая переменная имеет некорректное имя')

                if y.find(name) != -1:
                    raise ValueError('Вторая переменная имеет некорректное имя')
        else:
            raise ValueError('Имя содержит что-то кроме букв латиницей и цифр или начинается с цифры')
    if x == y:
        raise ValueError('Введены одинаковые имена')
    return f'{x} {y}'


def check_expression(expression: str, variables: str) -> str:
    """
    Функция для проверки выражения на корректность. Принимает на вход строку с функцией
    в аналитическом виде, возвращает sympy выражение.

    Parameters:
    ------------
    expression: str
        Строка содержащая функцию для проверки.
    variables: str
        Строка, содержащие имена переменных.

    Returns:
    -------
    str
        Функция в виде строки.
    """

    variables = variables.split()

    expression = expression.strip()
    if expression.find('—') != -1:
        expression = expression.replace('—', '-')

    if expression.find('–') != -1:
        expression = expression.replace('–', '-')

    checker = compile(expression, '<string>', 'eval')  # Может выдать SyntaxError, если выражение некорректно
    allowed_names = list(allowed_operations) + list(variables)

    for name in checker.co_names:
        if name not in allowed_names:
            raise NameError(f"The use of '{name}' is not allowed")

    x, y = symbols(f'{variables[0]} {variables[1]}')
    d = {variables[0]: x, variables[1]: y, 'e': math.e, 'pi': math.pi}
    function = sympify(expression, d, convert_xor=True)
    return str(function)


def check_limits(limits: str, split_by: Optional[str] = None) -> str:
    """
    Эта функция проверяет корректность введеных ограничений для переменных.

    Parameters:
    ------------
    limits: str
        Строка сожержащая ограничения слева и справа для переменной.
    split_by: Optional[str] = None
        Символ, которым разделяются ограничения.

    Returns:
    -------
    str
        Строка с ограничениями, разделенными пробелом.
    """

    if limits == 'None':
        return 'None'

    if limits.find('—') != -1:
        limits = limits.replace('—', '-')

    if limits.find('–') != -1:
        limits = limits.replace('–', '-')
    if len(limits.split(split_by)) != 2:
        raise ValueError('Неправильный формат ввода')
    else:
        limits = limits.split(split_by)
    pattern = re.compile(f'^[-]?[0-9]+[.]?[0-9]*$')
    for i in range(len(limits)):
        k = limits[i].strip()
        if not (k == '-oo' or k == '+oo' or pattern.match(limits[i])):
            raise ValueError('Неправильно задана одна из границ')
        else:
            if k == '+oo':
                limits[i] = inf
            elif k == '-oo':
                limits[i] = -inf
            else:
                limits[i] = float(limits[i])
    if limits[0] > limits[1]:
        raise ValueError('Левая граница превосходит правую')
    return f'{limits[0]} {limits[1]}'


def check_restr_func(expression: str, variables: str) -> str:
    """
    Функция проверяет корректность ввода для ограничивающей функции.

    Parameters:
    ------------
    s: str
        Строка, содержащая введеную функцию.
    variables: str
        Строка, содержащие имена переменных.

    Returns:
    -------
    str
        Функция в виде строки.
    """

    variables = variables.split()

    expression = expression.strip()
    if expression.find('—') != -1:
        expression = expression.replace('—', '-')

    if expression.find('–') != -1:
        expression = expression.replace('–', '-')

    checker = compile(expression, '<string>', 'eval')  # Может выдать SyntaxError, если выражение некорректно
    allowed_names = list(allowed_operations) + list(variables)

    flag_variables = True
    for name in checker.co_names:
        if name not in allowed_names:
            raise NameError(f"The use of '{name}' is not allowed")
        if name in variables and flag_variables:
            flag_variables = False
    if flag_variables:
        raise ValueError('Ограничивающая функция не содержит ни одной переменной')

    x, y = symbols(f'{variables[0]} {variables[1]}', real=True)
    d = {variables[0]: x, variables[1]: y, 'e': math.e, 'pi': math.pi}
    function = sympify(expression, d, convert_xor=True)
    if not sp.solve(function, [x, y]):
        raise ValueError('Неверный ввод ограничивающей функции')
    return str(function)
