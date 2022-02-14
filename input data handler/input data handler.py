import keyword
import re
import math
import sympy
from sympy import symbols, sympify, lambdify

a = {
    k: v for k, v in math.__dict__.items() if not k.startswith("__") and not
    (k == 'nan' or k == 'inf')
}
b = {
    k: v for k, v in sympy.__dict__.items() if not k.startswith("__") and
                                               type(v) == sympy.core.function.FunctionClass
}
allowed_operations = list(set(a.keys())|set(b.keys())) + ['pi', 'e']

def check_variables(variables, n_var = 2, split_by = None,
                    forbidden_names = allowed_operations):
    forbidden_names.extend(keyword.kwlist)
    if len(variables.split(split_by)) != n_var:
        raise ValueError('Некорректный ввод: введено болеее 2 переменных или имена содержат пробелы')
    else:
        x, y = variables.split(split_by)
        correct_name_filter = re.compile(f'^[a-zA-Z]+[0-9]?$')
        if bool(correct_name_filter.match(x)) and bool(correct_name_filter.match(y)):
            for forbidden_world in forbidden_names:
                if x.find(forbidden_world) != -1:
                    raise ValueError('Первая переменная имеет некорректное имя')
                    break
                if y.find(forbidden_world) != -1:
                    raise ValueError('Вторая переменная имеет некорректное имя')
                    break
        else:
            raise ValueError('Имя содержит что-то кроме букв латиницей и цифр или начинается с цифры')
    return x, y

def check_expression(expression, var1, var2, operations = allowed_operations):
    expression = expression.strip()
    if expression.find('—') != -1:
        print('Обнаружен символ "—". Автоматически распознан как знак минуса.')
        expression = expression.replace('—', '-')
    if expression.find('–') != -1:
        print('Обнаружен символ "–". Автоматически распознан как знак минуса.')
        expression = expression.replace('–', '-')
    code = compile(expression, '<string>', 'eval') # Может выдать SyntaxError, если выражение некорректно
    allowed_names = list(operations) + [var1, var2]
    for name in code.co_names:
        if name not in allowed_names:
            raise NameError(f"The use of '{name}' is not allowed")
    x, y = symbols(f'{var1} {var2}')
    d = {}
    d[f'{var1}'] = x
    d[f'{var2}'] = y
    function = sympify(expression, d, convert_xor = True)
    return function
