from typing import Optional

from sympy import symbols, sympify, lambdify
from numpy import inf


def prepare_data(vars: str, func: str, interval_x: Optional[str] = None, interval_y: Optional[str] = None,
                 g_func: Optional[str] = None):
    """
    Функция преобразовывает данные для передачи в конструктор класса.

    Parameters
    ----------
    vars: str
        Строка с переменными, разделенными пробелом.
    func: str
        Строка с функцией.
    interval_x: str
        Ограничения для первой переменной.
    interval_y: str
        Ограничения для второй переменной.
    g_func: str
        Ограничивающая функция в виде строки.

    Returns
    --------
    dict
        Набор параметров в виде словаря с данными, подготовленными для поиска экстремума.
    """

    sympy_vars = symbols(vars)
    vars = vars.split()
    func = sympify(func)
    func = func.subs({vars[0]: sympy_vars[0], vars[1]: sympy_vars[1]})
    interval_x = prepare_limits(interval_x)
    interval_y = prepare_limits(interval_y)
    param = {'vars': sympy_vars,
             'func': func,
             'interval_x': interval_x,
             'interval_y': interval_y}
    if g_func:
        g_func = sympify(g_func).subs({vars[0]: sympy_vars[0], vars[1]: sympy_vars[1]})
        param.update(g_func=g_func)
    return param


def prepare_limits(limits):
    """
    Функция преобразует ограничения в нужный вид.

    Parameters
    ----------
    limits: str
        Строка с числами, разделенными пробелом.

    Returns
    -------
    list
        Ограничения для функции.
    """

    if limits and limits != 'None':
        limits = limits.split()
        for i in range(2):
            if limits[i] == 'inf':
                limits[i] = inf
            elif limits[i] == '-inf':
                limits[i] = -inf
            else:
                limits[i] = float(limits[i])
        return limits


if __name__ == '__main__':
    c = prepare_data('x y', 'x**2 + y**2', '-10 10', '-10 10')
    print(type(c[0][0]))
    print(c[1].subs({c[0][0]: 1, c[0][1]: 2}))
