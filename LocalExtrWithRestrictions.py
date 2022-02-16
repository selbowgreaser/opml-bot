from Solution import Solution
import sympy as sm
import pandas as pd
from drawing_func import *
import numpy as np


class LocalExtrWithRestrictions(Solution):
    def __init__(self, variables, func, g_func, restr=False, interval_x=None, interval_y=None):

        x, y = sm.symbols('x y', real=True)
        self.func = func.subs({variables[0]: x, variables[1]: y})
        self.g_func = g_func.subs({variables[0]: x, variables[1]: y})
        self.variables = [x, y]
        self.restr = restr
        self.interval_x = interval_x
        self.interval_y = interval_y

    def solve(self):

        x, y = sm.symbols('x y', real=True)

        lagrange_func = self.func
        lam = sm.symbols('lam')
        lagrange_func = lagrange_func + lam * self.g_func

        equations = []
        for var in self.variables:
            equations.append(lagrange_func.diff(var))

        equations.append(lagrange_func.diff(lam))

        solutions = sm.solve(equations, self.variables + [lam], dict=True)
        relevant_critical_dots = []

        for solution in solutions:

            if self.interval_x is not None and self.interval_y is not None:

                if (self.interval_x[0] <= solution[x] <= self.interval_x[1]) and \
                        (self.interval_y[0] <= solution[y] <= self.interval_y[1]):
                    relevant_critical_dots.append(solution)
            elif self.interval_x is not None:
                if self.interval_x[0] <= solution[x] <= self.interval_x[1]:
                    relevant_critical_dots.append(solution)

            elif self.interval_y is not None:
                if self.interval_y[0] <= solution[y] <= self.interval_y[1]:
                    relevant_critical_dots.append(solution)
            else:
                relevant_critical_dots = solutions

        hessian = sm.Matrix([[0, self.g_func.diff(x), self.g_func.diff(y)],
                             [self.g_func.diff(x), lagrange_func.diff(x).diff(x),  lagrange_func.diff(x).diff(y)],
                             [self.g_func.diff(y), lagrange_func.diff(x).diff(y), lagrange_func.diff(y).diff(y)]])

        output = pd.DataFrame(columns=['dots', '|H|', 'value'])

        min_x_y = [np.inf, np.inf]
        max_x_y = [-np.inf, -np.inf]
        critical_dots_for_draw = []
        for i, dot in enumerate(relevant_critical_dots):
            output.loc[i] = [(dot[x], dot[y]), hessian.subs(dot).det(), self.func.subs(dot)]
            critical_dots_for_draw.append((float(dot[x]), float(dot[y]), float(self.func.subs(dot))))
            min_x_y = [min(min_x_y[0], dot[x]), min(min_x_y[1], dot[y])]
            max_x_y = [max(max_x_y[0], dot[x]), max(max_x_y[1], dot[y])]

        min_x_y = [float(min_x_y[0] - 5), float(min_x_y[1] - 5)]
        max_x_y = [float(max_x_y[0] + 5), float(max_x_y[1] + 5)]

        def type_dot(h_det):
            if h_det > 0:
                return 'max'
            elif h_det < 0:
                return 'min'
            else:
                return 'saddle'

        output['type_dot'] = output['|H|'].apply(lambda dot_i: type_dot(dot_i))

        if self.interval_x is None:
            self.interval_x = [min_x_y[0], max_x_y[0]]

        if self.interval_y is None:
            self.interval_y = [min_x_y[1], max_x_y[1]]

        data_for_draw = make_df_for_drawing(sm.lambdify([x, y], self.func), self.interval_x, self.interval_y)
        plot = draw_3d(data_for_draw, critical_dots_for_draw)
        plot.write_image('graph.png', width=2048, height=1024)

        def make_output_str(row):
            dot_str = '(' + str(round(float(row.dots[0]), 3)) + ', ' + str(round(float(row.dots[1]), 3)) + ')'
            return dot_str + ' - ' + row.type_dot

        output = output[['dots', 'type_dot']].apply(make_output_str, axis=1)
        if output.shape[0] > 0:
            return output.to_list()

        else:
            return 'Решений нет'
