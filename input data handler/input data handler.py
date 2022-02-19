import re
import math
import sympy
from sympy import symbols, sympify, lambdify
from operations_name_gen import allowed_operations, forbidden_names_for_variables
from numpy import inf


def check_variables(variables, split_by=None):
    """

    Функция для проверки переменных на корректность имени. На вход /
    принимает строку с переменными, после проверки возвращает отдельно /
    первую и вторую переменные.

    Parameters:
    ------------
    variables: str
        String with 2 variables names
    split_by: str, optional
        The character that split values. Default works like Python string .split() method

    Returns
    -------
    tuple of string variable's names
    """
    if len(variables.split(split_by)) != 2:
        raise ValueError('Некорректный ввод: введено болеее 2 переменных или имена содержат пробелы')
    else:
        x, y = variables.split(split_by)
        correct_name_filter = re.compile(f'^[a-zA-Z]+[0-9]?$')

        if bool(correct_name_filter.match(x)) and bool(correct_name_filter.match(y)):
            for name in forbidden_names_for_variables:

                if x.find(name) != -1:
                    raise ValueError('Первая переменная имеет некорректное имя')

                if y.find(name) != -1:
                    raise ValueError('Вторая переменная имеет некорректное имя')
        else:
            raise ValueError('Имя содержит что-то кроме букв латиницей и цифр или начинается с цифры')
    return (x, y)

def check_expression(expression, variables):
    """

    Функция для проверки выражения на корректность. Принимает на вход /
    строку с функцией в аналитическом виде, возвращает sympy выражение.

    Parameters:
    ------------
    expression: str
        The string with function to check
    variables: array-like
        Array of variables names (name as string)

    Returns
    -------
    input function as sympy expression
    """
    expression = expression.strip()
    if expression.find('—') != -1:
        print('Обнаружен символ "—". Автоматически распознан как знак минуса.')
        expression = expression.replace('—', '-')

    if expression.find('–') != -1:
        print('Обнаружен символ "–". Автоматически распознан как знак минуса.')
        expression = expression.replace('–', '-')

    checker = compile(expression, '<string>', 'eval') # Может выдать SyntaxError, если выражение некорректно
    allowed_names = list(allowed_operations) + list(variables)

    for name in checker.co_names:
        if name not in allowed_names:
            raise NameError(f"The use of '{name}' is not allowed")

    x, y = symbols(f'{variables[0]} {variables[1]}')
    d = {variables[0]: x, variables[1]: y, 'e': math.e, 'pi': math.pi}
    function = sympify(expression, d, convert_xor = True)
 #   function = lambdify([x, y], function)
    return function

def check_limits(limits, split_by=None):
    """

    Эта функция проверяет корректность введеных ограничений для переменных.
    Возвращает котреж ограничений.

    Parameters:
    ------------
    limits: str
        string with variable limits
    split_by: str, optional
        character that divide left limit from right.
        Default works like Python string .split() method

    Returns
    -------
    tuple of limits


    """
    if limits.find('—') != -1:
        limits = limits.replace('—', '-')

    if limits.find('–') != -1:
        limits = limits.replace('–', '-')
    if len(limits.split(split_by)) != 2:
        raise ValueError('Неправильный формат ввода')
    else:
        limits = limits.split(split_by)
    pattern = re.compile(f'^[-]?[0-9]+[\.]?[0-9]*$')
    for i in range(len(limits)):
        k = limits[i].strip()
        if not (k == '-oo' or k == 'oo' or bool(pattern.match(limits[i]))):
            raise ValueError('Неправильно задана одна из границ')
        else:
            if k == 'oo':
                limits[i] = inf
            elif k == '-oo':
                limits[i] = -inf
            else:
                limits[i] = float(limits[i])
    if limits[0] > limits[1]:
        raise ValueError('Левая граница превосходит правую')
    return tuple(limits)

