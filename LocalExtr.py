import pandas as pd
import numpy as np
from Solution import Solution
from drawing_func import *
import sympy as sp


class LocalExtr(Solution):
    def __init__(self, vars, func, restr=False, interval_x=None, interval_y=None):
        self.vars = sp.symbols(vars, real=True)
        vars = vars.split()
        self.func = sp.sympify(func).subs({vars[0]: self.vars[0], vars[1]: self.vars[1]})

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
        self.points = self.critical_points()
        if self.restr:
            self.points = self.points.append(self.border_points(),
                                             ignore_index=True)
        ans = ''
        if self.points.empty:
            ans += 'Решений нет'
            # здесь же указать лимиты
        else:
            f = lambda x: list(zip(x['x'].values, x['y'].values, x['z'].values))
            to_output = self.points.groupby(by='type', axis=0)[['x', 'y', 'z']].apply(f)
            for i, v in enumerate(to_output):
                ans += f'{to_output.index[i]}: {v}\n'
            # дописать график функции!

        return ans

    def check_point(point, xlim, ylim):

        """Метод проверяет точку на соответствие лимитам для координат.

        Параметры
        ---------
        point : array-like
            массив с координатами точки вида (x, y)
        xlim : array-like
            массив с ограничениями слева и справа типа float
            или np.inf для первой координаты
        ylim : array-like
            массив с ограничениями слева и справа типа float
            или np.inf для первой координаты

        Возвращаемое значение
        ---------------------
        True если точка соответствует ограничениям или их нет
        иначе False

        """

        def check_cord(cord, cordlim):

            """Функция проверяет сооответствие координаты ее пределам.

            Параметры
            ---------
            cord : float
                координата
            cordlim : array-like or None
                    массив с ограничениями слева и справа типа float
                    или np.inf

            Возвращаемое значение
            ---------------------
            True если координата соответствует ограничениям или их нет
            иначе False

            """

            if cordlim[0] <= cord <= cordlim[1]:
                return True
            else:
                return False

        if xlim and ylim:
            return check_cord(point[0], xlim) \
                   and check_cord(point[1], ylim)
        elif xlim:
            return check_cord(point[0], xlim)
        elif ylim:
            return check_cord(point[1], ylim)
        else:
            return True

    def critical_points(self):

        """Метод находит критические точки для задачи.

        С помощью производных находятся все экстремумы.

        Возвращаемое значение
        ----------------------
        pd.DataFrame, с колонками x, y, z

        """

        def set_dot_type(data, d, d2x):

            """Функция определяет тип точки.

            При помощи вторых производных функция определяет
            является ли точка минимальной/максимальной/седловой.
            Используется для передачи в метод pandas.DataFrame.apply().

            Параметры
            ---------
            data: pd.Series
                столбцы со значениями x, y, z
            d: sympy выражение
                детерминант матрицы вторых производных. В него
                подставлются значения в точках
            d2x: sympy выражение
                вторая производная по икс. В него подставляется
                значения в точках

            Возвращаемое значение
            ---------------------
            pd.Series со значениями одним из четырех типов точки:
            'saddle', 'global min', 'global msx', 'unknown'
            """
            d = d.subs({x: data[0], y: data[1]})
            d2x = d2x.subs({x: data[0], y: data[1]})

            if d < 0:
                return 'saddle'
            elif d > 0 and d2x > 0:
                return 'global min'
            elif d > 0 and d2x < 0:
                return 'global max'
            else:
                return 'unknown'

        x, y = self.vars[0], self.vars[1]
        z = self.func
        critical_points_sympy = sp.solve([z.diff(x), z.diff(y)], [x, y], dict=True)
        f = sp.lambdify([x, y], z)
        critical_points = pd.DataFrame(columns=['x', 'y', 'z'])

        for i in critical_points_sympy:
            i = [float(i[x]), float(i[y])]
            if LocalExtr.check_point(i, self.interval_x, self.interval_y):
                point = {'x': i[0], 'y': i[1], 'z': f(i[0], i[1])}
                critical_points = critical_points.append(point, ignore_index=True)

        if not critical_points.empty:
            D = z.diff(x, 2) * z.diff(y, 2) - z.diff(x).diff(y) ** 2
            D2x = z.diff(x, 2)
            critical_points['type'] = critical_points.apply(set_dot_type,
                                                            axis=1,
                                                            args=(D, D2x))
        else:
            critical_points['type'] = []

        return critical_points

    def find_local_extr(self, free_var_ind):

        """Метод находит локальные экстремумы.

        Пераметры
        ---------
        free_var_ind: 0 or 1
            Номер переменной, которая является свободной
            (по ней нет ограничений)

        Возвращаемое значение
        ---------------------
        pd.DataFrame с колонками как координаты точек x, y, z

        """
        points = pd.DataFrame(columns=['x', 'y', 'z'])

        if free_var_ind == 0:
            lim = self.interval_y
            free_var = self.vars[0]
            limit_var = self.vars[1]
        elif free_var_ind == 1:
            lim = self.interval_x
            free_var = self.vars[1]
            limit_var = self.vars[0]

        for i in lim:
            if abs(i) == np.inf:
                continue
            else:
                fun = self.func.subs({limit_var: i})
                potential_points = sp.solve(fun.diff(free_var), free_var, dict=True)
                for j in potential_points:
                    coord = float(j[free_var])
                    if free_var_ind == 0:
                        point = (coord, i)
                    else:
                        point = (i, coord)

                    if LocalExtr.check_point(point,
                                             self.interval_x,
                                             self.interval_y):
                        try:
                            z = float(fun.subs(j))
                        except ZeroDivisionError:
                            pass
                        else:
                            points = points.append({'x': point[0],
                                                    'y': point[1],
                                                    'z': float(fun.subs(j))},
                                                   ignore_index=True)
        return points

    def border_points(self):

        """Метод находит локальные экстремумы, обходя все
        возможные границы.

        Возвращаемое значение
        ---------------------
        pd.DataFrame с колонками x, y, z, type.
        type содержит либо 'local max' либо 'local min'

        """
        f = sp.lambdify(self.vars, self.func)

        if self.points.empty:
            min_z = np.inf
            max_z = -np.inf
        else:
            min_z = self.points['z'].min()
            max_z = self.points['z'].max()

        points = pd.DataFrame(columns=['x', 'y', 'z'])

        if self.interval_x and self.interval_y:
            for x in self.interval_x:
                for y in self.interval_y:
                    if abs(x) == np.inf or abs(y) == np.inf:
                        continue
                    else:
                        try:
                            z = f(x, y)
                        except ZeroDivisionError:
                            pass
                        else:
                            point = {'x': x, 'y': y, 'z': f(x, y)}
                            points = points.append(point, ignore_index=True)
            points = points.append(self.find_local_extr(0), ignore_index=True)
            points = points.append(self.find_local_extr(1), ignore_index=True)
        elif self.interval_x:
            points = points.append(self.find_local_extr(1), ignore_index=True)
        elif self.interval_y:
            points = points.append(self.find_local_extr(0), ignore_index=True)

        points = points.drop_duplicates()
        cond = ((points['z'] == points['z'].max()) & (points['z'] > max_z)) \
               | ((points['z'] == points['z'].min()) & (points['z'] < min_z))
        points = points[cond]
        points['type'] = np.where(points['z'] == points['z'].max(),
                                  'local max',
                                  'local min')
        return points

if __name__ == '__main__':
    eq = LocalExtr('x y', 'x**2 - y**2', True, '-10 10', '-10 10')
    solve = eq.solve()
    print(solve) #
