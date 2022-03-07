from sympy import symbols, sympify, lambdify
from numpy import inf

def prepare_data(vars, func, interval_x=None, interval_y=None, g_func = None):
    sympy_vars = symbols(vars)
    vars = vars.split()
    func = sympify(func)
    func = func.subs({vars[0]: sympy_vars[0], vars[1]: sympy_vars[1]})
    interval_x = prepare_limits(interval_x)
    interval_y = prepare_limits(interval_y)
    if g_func:
        g_func = sympify(g_func).subs({vars[0]: sympy_vars[0], vars[1]: sympy_vars[1]})
        return vars, func, interval_x, interval_y, g_func
    else:
        return vars, func, interval_x, interval_y


def prepare_limits(limits):
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
    print(c[1].subs({c[0][0]: 1, c[0][1]: 2}))
