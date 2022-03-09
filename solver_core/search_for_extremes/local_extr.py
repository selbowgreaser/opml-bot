import pandas as pd
import numpy as np
import sympy as sp

from .drawing_func import *


class LocalExtr:
    """
    Решатель задачи.

    Parameters
    ----------
    vars : list
        Список переменных из sympy.symbols.
    func : sympy выражение
        Функция.
    interval_x: tuple
        Кортеж с пограничными точками для оси X.
    interval_y: tuple
        Кортеж с пограничными точками для оси Y.
    """
    def __init__(self, vars, func, restr=False, interval_x=None, interval_y=None):
        self.vars = vars
        self.func = func
        self.restr = restr
        self.interval_x = interval_x
        self.interval_y = interval_y

    def generate_colors(self):
        """
        Метод создает раскраску для точек.

        Returns
        --------
        pd.Series
            Цвета по типам экстремумов.
        """

        dots_types = ['global min', 'local min', 'saddle', 'local max',
                      'global max', 'unknown']
        colors = ['rgb(228,26,28)', 'rgb(77,175,74)',
                   'rgb(152,78,163)', 'rgb(255,127,0)',
                   'rgb(255,255,51)', 'rgb(166,86,40)']
        colors_dict = dict(zip(dots_types, colors))
        set_color = lambda x: colors_dict[x]
        colors = self.points['types'].apply(set_color)
        return colors

    def solve(self) -> str:
        """
        Метод решает задачу локального экстремума.

        Returns
        -------
        str
            Строка с ответом.
        """

        self.points = self.critical_points()
        if self.restr:
            self.points = self.points.append(self.border_points(),
                                             ignore_index=True)
            self.points = self.points.drop_duplicates(['x', 'y', 'z'])
        ans = ''
        if self.points.empty:
            ans += 'Решений нет'
            if not self.interval_x:
                self.interval_x = (-1, 1)  # значения для интервалов, если они не заданы и нет точек
            if not self.interval_y:
                self.interval_y = (-1, 1)
        else:
            f = lambda x: list(zip(x['x'].values, x['y'].values, x['z'].values))
            to_output = self.points.groupby(by='type', axis=0)[['x', 'y', 'z']].apply(f)
            for i, v in enumerate(to_output):
                ans += f'{to_output.index[i]}: {v}\n'
            if not self.interval_y:
                self.interval_y = (self.points['y'].min() - 5, self.points['y'].max() + 5)
            if not self.interval_x:
                self.interval_x = (self.points['x'].min() - 5, self.points['x'].max() + 5)

        self.points = self.points.rename(columns={'type': 'types'})
        self.points['color'] = self.generate_colors()

        data_for_draw = make_df_for_drawing(self.func, self.vars,
                                            self.interval_x, self.interval_y)
        plot = draw_3d(data_for_draw, critical_points=self.points)
        save_fig_to_pic(plot, 'graph', ['html'])
        return ans

    def check_point(point, xlim, ylim):
        """
        Метод проверяет точку на соответствие лимитам для координат.

        Parameters
        ---------
        point : array-like
            Массив с координатами точки вида (x, y), координата z не обязательна
        xlim : array-like
            Массив с ограничениями слева и справа типа float
            или np.inf для первой координаты
        ylim : array-like
            массив с ограничениями слева и справа типа float
            или np.inf для второй координаты

        Returns
        -------
        bool
            True если точка соответствует ограничениям или их нет, иначе False
        """

        def check_cord(cord: float, cordlim: list):
            """
            Функция проверяет сооответствие координаты ее пределам.

            Parameters
            ---------
            cord : float
                Координата.
            cordlim : array-like or None
                Массив с ограничениями слева и справа типа float или np.inf

            Returns
            -------
            bool
                True если координата соответствует ограничениям или их нет, иначе False.
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
        """
        Метод находит критические точки для задачи.

        С помощью производных находятся все экстремумы.

        Returns
        -------
        pd.DataFrame
            Данные о критических точках.
        """

        def set_dot_type(data, d, d2x):
            """
            Функция определяет тип точки.

            При помощи вторых производных функция определяет
            является ли точка минимальной/максимальной/седловой.
            Используется для передачи в метод pandas.DataFrame.apply().

            Parameters
            ----------
            data: pd.Series
                Столбцы со значениями x, y, z.
            d: sympy выражение
                Детерминант матрицы вторых производных. В него подставлются значения в точках
            d2x: sympy выражение
                Вторая производная по икс. В него подставляется значения в точках

            Returns
            -------
            pd.Series
                Серия со значениями одним из четырех типов точки: 'saddle', 'global min', 'global max', 'unknown'
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

    def find_local_extr(self, free_var_ind, max_val, min_val):
        """
        Метод находит локальные экстремумы.

        Parameters
        ----------
        free_var_ind: 0 or 1
            Номер переменной, которая является свободной (по ней нет ограничений)
        max_val: float or np.inf
            Максимальное значение. В случае если в ходе решения окажется, что у функции есть супремум,
            больший чем это значение, то максимальное значение
            для всех локальных экстремумов будет обновлено.
        min_val: float or np.inf
            Аналогично как для min_val, только минимум и инфимум.

        Returns
        -------
        pd.DataFrame
            с колонками как координаты точек x, y, z
            max_value - новое максимальное значение
            min_value - новое минимальное значение
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
                if fun == sp.zoo:
                    check = sp.limit(self.func, limit_var, i)
                    if check > max_val:
                        max_val = float(check)
                    if check < min_val:
                        min_val = float(check)
                    continue
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
                            if z > max_val:
                                max_val = z
                            if z < min_val:
                                min_val = z
                            points = points.append({'x': point[0],
                                                    'y': point[1],
                                                    'z': z},
                                                   ignore_index=True)
        return points, max_val, min_val

    def border_points(self):
        """
        Метод находит локальные экстремумы, обходя все
        возможные границы.

        Returns
        -------
        pd.DataFrame
            С колонками x, y, z, type. type содержит либо 'local max' либо 'local min'
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
                            values = [x, y]
                            for i in range(2):
                                check = self.func.subs({self.vars[i]: values[i]})
                                lim = sp.limit(check, self.vars[1 - i], values[1 - i])
                                try:
                                    a = float(lim)
                                    if a > max_z:
                                        pass
                                        max_z = a
                                    elif a < min_z:
                                        min_z = a
                                except TypeError:
                                    pass
                        else:
                            point = {'x': x, 'y': y, 'z': f(x, y)}
                            points = points.append(point, ignore_index=True)
        if self.interval_x:
            a = self.find_local_extr(1, max_z, min_z)
            points = points.append(a[0], ignore_index=True)
            max_z = a[1]
            min_z = a[2]
        if self.interval_y:
            a = self.find_local_extr(0, max_z, min_z)
            points = points.append(a[0], ignore_index=True)
            max_z = a[1]
            min_z = a[2]
        points = points.drop_duplicates()
        cond = ((points['z'] == points['z'].max()) & (points['z'] >= max_z)) \
               | ((points['z'] == points['z'].min()) & (points['z'] <= min_z))
        points = points[cond]
        points['type'] = np.where(points['z'] == points['z'].max(),
                                  'local max',
                                  'local min')
        return points


if __name__ == '__main__':
    from solver_core.search_for_extremes.handlers.preprocessing import prepare_data
    data = prepare_data('x y', 'x**2 - y**2', interval_x='-10 10', interval_y='-10 10')
    print(data[0][0])
    print(type(data[0][0]))
    eq = LocalExtr(vars=data[0], func=data[1], restr=True,
                   interval_x=data[2], interval_y=data[3])
    solve = eq.solve()
    print(solve)
