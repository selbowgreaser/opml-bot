import pandas as pd
import numpy as np
from Solution import Solution
from drawing_func import *
from sympy import *


class LocalExtr(Solution):

    def __init__(self, vars, func, restr=False, interval_x=None, interval_y=None):
        """


        :param vars: список с названием переменных в виде строки (тут не как у Вити)
        :param func: sympy функция
        :param restr: bool
        :param interval_x: array-like
        :param interval_y: array-like
        """
        self.vars = vars
        self.func = func
        self.restr = restr
        self.interval_x = interval_x
        self.interval_y = interval_y

    def solve(self):
        # x, y = sm.symbols(f'{self.vars[0]} {self.vars[1]}', real=True)
        x, y = self.vars[0], self.vars[1]
        z = self.func
        f = lambdify([x, y], self.func)
        critical_points_sympy = solve([z.diff(x), z.diff(y)], [x, y], dict=True)
        critical_points = []

        for i in critical_points_sympy:
            if self.interval_x and self.interval_y:
                if (self.interval_x[0] <= i[x] <= self.interval_x[1]) and (
                        self.interval_y[0] <= i[y] <= self.interval_y[1]):
                    critical_points.append((i[x], i[y], f(i[x], i[y])))
            elif self.interval_x:
                if (self.interval_x[0] <= i[x] <= self.interval_x[1]):
                    critical_points.append((i[x], i[y], f(i[x], i[y])))
            elif self.interval_y:
                if (self.interval_y[0] <= i[y] <= self.interval_y[1]):
                    critical_points.append((i[x], i[y], f(i[x], i[y])))
            else:
                critical_points.append((i[x], i[y], f(i[x], i[y])))

        D = z.diff(x, 2) * z.diff(y, 2) - z.diff(x).diff(y) ** 2
        D2x = z.diff(x, 2)
        extr = {'min': [], 'max': [], 'saddle': []}
        max_value = -np.inf
        min_value = np.inf

        for i in critical_points:
            i = [float(j) for j in i]
            d = D.subs({x: i[0], y: i[1]})
            d2x = D2x.subs({x: i[0], y: i[1]})
            if i[2] > max_value:
                max_value = i[2]
            if i[2] < min_value:
                min_value = i[2]
            if d < 0:
                extr['saddle'].append(i)
            elif d > 0 and d2x > 0:
                extr['min'].append(i)
            elif d > 0 and d2x < 0:
                extr['max'].append(i)
            else:
                critical_points.remove(i)

        if self.interval_x and self.interval_y:
            for i in self.interval_x:
                for j in self.interval_y:
                    if abs(i) == np.inf or abs(j) == np.inf:
                        continue
                    fun = f(i, j)
                    if fun > max_value:
                        border_points.append((i, j, fun))
                    elif fun < min_value:
                        border_points.append((i, j, fun))
        if self.interval_x:
            for i in self.interval_x:
                if abs(i) == np.inf:
                    continue
                fun = z.subs({x: i})
                point = solve(fun.diff(y), y, dict=True)
                for j in point:
                    y_check = j[y]
                    if self.interval_y:
                        if not (self.interval_y[0] <= y_check <= self.interval_y[1]):
                            continue
                    check = fun.subs({y: y_check})
                    if check > max_value:
                        border_points.append((float(i), float(y_check), float(check)))
                    elif check < min_value:
                        border_points.append((float(i), float(y_check), float(check)))
        if self.interval_y:
            for i in self.interval_y:
                if abs(i) == np.inf:
                    continue
                fun = z.subs({y: i})
                point = solve(fun.diff(x), x, dict=True)
                for j in point:
                    x_check = j[x]
                    if self.interval_x:
                        if not (self.interval_x[0] <= x_check <= self.interval_x[1]):
                            continue
                    check = fun.subs({x: x_check})
                    if check > max_value:
                        border_points.append((float(x_check), float(i), float(check)))
                    elif check < min_value:
                        border_points.append((float(x_check), float(i), float(check)))

        if border_points:
            minimum_value = min(border_points, key=lambda x: x[2])[2]
            maximum_value = max(border_points, key=lambda x: x[2])[2]
            border_points = list(filter(lambda x: x[2] == minimum_value or x[2] == maximum_value, border_points))
            for i in border_points:
                if i[2] == minimum_value:
                    extr['min'].append(i)
                else:
                    extr['max'].append(i)
            critical_points = set(critical_points + border_points)
        ans = ''
        for i in extr:
            ans += f'{i}: {extr[i]}'
        if ans == '':
            ans = 'Решений нет'
        if self.interval_x:
            self.interval_x = [min(critical_points, key=lambda t: t[0])[0] - 5,
                               min(critical_points, key=lambda t: t[1])[1] + 5]
        if self.interval_y:
            self.interval_y = [max(critical_points, key=lambda t: t[0])[0] - 5,
                               max(critical_points, key=lambda t: t[1])[1] + 5]

        data_for_draw = make_df_for_drawing(f, self.interval_x, self.interval_y)
        plot = draw_3d(data_for_draw, critical_points)
        plot.write_image('graph.png', width=2048, height=1024)

        return ans

if __name__ == '__main__':
    x1, x2 = sm.symbols('x1 x2')
    eq = LocalExtrWith([x1, x2], x1 ** 2 + 0.5 * x2 ** 2, x1 ** 3 + x2 ** 3 - 1)
    solve = eq.solve()
    print(solve[0])
    save_fig_to_pic(solve[1], 'test', ['png', 'html'])