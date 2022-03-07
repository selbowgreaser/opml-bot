from sympy import symbols, sympify, lambdify
from numpy import inf

def prepare_data(vars, func, interval_x=None, interval_y=None, g_func = None):
    """Функция преобразовывает данные для передачи в конструктор класса.

    Parameters
    ----------
    vars: str
        строка с переменными, разделенными пробелом
    func: str
        строка с фунцией
    imterval_x: str
        ограничения для первой переменной. границы разделенные пробелом
    interval_y: str
        ограничения для второй переменной
    g_func: str
        ограничивающая функция в виде строки
    Returns
    --------
    vars: список из двух sympy.Symbol
    func: sympy expression
    interval_x: список из значений типа float или np.inf
    imterval_y: список из значений типа dloat или np.inf
    g_func: sympy expression
    """

    sympy_vars = symbols(vars)
    vars = vars.split()
    func = sympify(func)
    func = func.subs({vars[0]: sympy_vars[0], vars[1]: sympy_vars[1]})
    interval_x = prepare_limits(interval_x)
    interval_y = prepare_limits(interval_y)
    if g_func:
        g_func = sympify(g_func).subs({vars[0]: sympy_vars[0], vars[1]: sympy_vars[1]})
        return sympy_vars, func, interval_x, interval_y, g_func
    else:
        return sympy_vars, func, interval_x, interval_y


def prepare_limits(limits):
    """Функция преобразует ограничения в нужный вид.

    Parameters
    ----------
    limits: str
        строка с числами, разделенными пробелом
    Returns
    -------
    list из двух float значений
    """

    if limits:
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
    #print(c)
    #print(c[1].subs({c[0][0]: 1, c[0][1]: 2}))
