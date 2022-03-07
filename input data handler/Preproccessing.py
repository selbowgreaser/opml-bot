from sympy import symbols, sympify, lambdify
from numpy import inf

def prepare_data(vars, func, interval_x, interval_y, g_func):
    sympy_vars = symbols(vars)
    vars = vars.split()
    func = sympify(func)
    func = func.subs({var})