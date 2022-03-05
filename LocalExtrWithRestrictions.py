from Solution import Solution
import sympy as sp
from drawing_func import *
import numpy as np


class LocalExtrWithRestrictions(Solution):

    def __init__(self, variables, func, g_func, restr=False, interval_x=None, interval_y=None):
        x, y = sp.symbols('x y', real=True)
        variables = variables.split()
        self.func = sp.sympify(func, {'e': np.e, 'pi': np.pi}).subs({variables[0]: x, variables[1]: y})
        self.g_func = sp.sympify(g_func, {'e': np.e, 'pi': np.pi}).subs({variables[0]: x, variables[1]: y})
        self.variables = [x, y]
        self.restr = restr
        self.interval_x = interval_x
        self.interval_y = interval_y

        if self.interval_x:
            self.interval_x = self.interval_x.split()
            for i in range(2):
                if self.interval_x[i] == 'inf':
                    self.interval_x[i] = np.inf
                elif self.interval_x[i] == '-inf':
                    self.interval_x[i] = -np.inf
                else:
                    self.interval_x[i] = float(self.interval_x[i])

        if self.interval_y:
            self.interval_y = self.interval_y.split()
            for i in range(2):
                if self.interval_y[i] == 'inf':
                    self.interval_y[i] = np.inf
                elif self.interval_y[i] == '-inf':
                    self.interval_y[i] = -np.inf
                else:
                    self.interval_y[i] = float(self.interval_y[i])

    def solve(self):
        pass
