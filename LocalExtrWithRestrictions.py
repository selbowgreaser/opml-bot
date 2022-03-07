from Solution import Solution
from drawing_func import *

import sympy as sp
import numpy as np
import pandas as pd
from IPython.display import display, Latex


class LocalExtrWithRestrictions(Solution):

    def __init__(self, variables, func, g_func, interval_x=None, interval_y=None):
        """
        Конструктор задачи. Нужно передать обязательно список переменных, основную и ограничивающую функции
        Интервалы при отсутствии будут определены автоматически
        :param variables: list из sympy.symbols
        :param func: sympy выражение
        :param g_func: sympy выражение
        :param interval_x: tuple с числами
        :param interval_y: tuple с числами
        """

        x, y = sp.symbols('x y')
        self.func = func.subs({variables[0]: x, variables[1]: y})
        self.g_func = g_func.subs({variables[0]: x, variables[1]: y})
        self.variables = [x, y]
        self.interval_x = interval_x
        self.interval_y = interval_y
        self.lam = sp.symbols('lambda')

    def f_lagrange(self, display_flag=False):
        """
        Создает функцию Лагранжа
        :param display_flag: флаг вывода в дисплей функции Лагражна. True - вывести, False - нет
        :return: Функцию Лагранжа
        """
        lagrange_func = self.func
        lam = self.lam
        lagrange_func = lagrange_func + lam * self.g_func

        if display_flag:
            display(Latex(r'$\text{Составим функцию Лагранжа}$'))
            display(Latex(r'$\displaystyle L(x,y,\lambda) = ' + sp.latex(lagrange_func) + '$'))

        return lagrange_func

    def system(self, display_flag=False):
        """
        Составляет системы из частных производных функции Лагранжа
        :param display_flag: флаг вывода в дисплей системы уравнений. True - вывести, False - нет
        :return: Систему уравнений
        """
        lagrange_func = self.f_lagrange(True)
        lam = self.lam

        equations = []
        for var in self.variables:
            equations.append(lagrange_func.diff(var))

        equations.append(lagrange_func.diff(lam))

        if display_flag:
            display(Latex(r'$\text{Решим систему из трех уравнений: }$'))
            long_row = r"$\displaystyle \begin{cases} \displaystyle\frac{\partial L}{\partial x} = " +\
                       sp.latex(equations[0]) + r' = 0\\' +\
                       r"\displaystyle\frac{\partial L}{\partial y} = " + sp.latex(equations[1]) + r' = 0\\' +\
                       r"\displaystyle\frac{\partial L}{\partial \lambda} = " +\
                       r"\displaystyle " + sp.latex(equations[2]) + r" = 0 \end{cases} $"

            display(Latex(long_row))

        return equations

    def solve_system(self):
        """
        Вызывает составитель системы self.system, затем решает его и выделяет точки, которые являются вещественными
        и находятся в нужных интервалах.
        :return: real_solutions, indices - точки и их номера для вывода. Например, если точка M3 и M5 подошли, то в
                 indices есть 3 и 5 - числа, остальные числа не находятся.
        """
        lam = self.lam
        system = self.system(True)
        solutions = sp.solve(system, self.variables + [lam], dict=True)
        x, y = self.variables

        real_solutions = []
        indices = []

        display(Latex(r'$ \text{Найденные точки:} $'))
        i = False
        for i, sol in enumerate(solutions):
            display_row = r'$\displaystyle \mathrm{M}' + f'_{i + 1}' + r'\left('
            display_row += sp.latex(sol[x]) + r', '
            display_row += sp.latex(sol[y]) + r', '
            display_row += sp.latex(sol[lam]) + r'\right) $'
            display(Latex(display_row))

            if bool(sol[x].is_real) and bool(sol[y].is_real) and bool(sol[lam].is_real):
                if self.point_check(sol):
                    real_solutions.append(sol)
                    indices.append(i)
        if not i:
            display(Latex(r'$\text{Решений системы нет}$'))

        return real_solutions, indices

    def point_check(self, point):
        """
        Получает точку с вещественными значением и проверяет подходят ли она в ограничения
        :param point: точка
        :return: bool - подходит точка или нет
        """
        x, y = self.variables

        if self.interval_x is not None and self.interval_y is not None:

            check_x = self.interval_x[0] <= point[x] <= self.interval_x[1]
            check_y = self.interval_y[0] <= point[y] <= self.interval_y[1]
            if check_x and check_y:
                return True

        elif self.interval_x is not None:
            if self.interval_x[0] <= point[x] <= self.interval_x[1]:
                return True

        elif self.interval_y is not None:
            if self.interval_y[0] <= point[y] <= self.interval_y[1]:
                return True
        else:
            return True

        return False

    def gen_hessian(self):
        """
        Генерирует гессиан. Вызывает self.f_lagrange, затем составляет матрицу-гессиан и возвращает его
        :return: гессиан
        """
        x, y = self.variables
        lagrange_func = self.f_lagrange()

        hessian = sp.Matrix([[0, self.g_func.diff(x), self.g_func.diff(y)],
                             [self.g_func.diff(x), lagrange_func.diff(x).diff(x), lagrange_func.diff(x).diff(y)],
                             [self.g_func.diff(y), lagrange_func.diff(x).diff(y), lagrange_func.diff(y).diff(y)]])

        return hessian

    @staticmethod
    def type_dot(h_det: float):
        """
        Проверяет тип точки и выдает ее название и цвет
        :param h_det: значение детерминанта гессиана - вещественное число
        :return: словарь со значение типа и цвета
        """
        if h_det > 0:
            return {"type": 'max', "color": 'red'}
        elif h_det < 0:
            return {"type": 'min', "color": 'lightgreen'}
        else:
            return {"type": 'saddle', "color": 'yellow'}

    def solve(self):
        """
        Основной метод, собирает все пункты решения в один.
        :return: pd.DataFrame с вещественными точками и график plotly
        """
        x, y = self.variables
        hessian = self.gen_hessian()
        relevant_points, indices = self.solve_system()
        self.min_max(relevant_points)

        if len(relevant_points):
            display(Latex(r'$ \displaystyle \text{Составим Гессиан: }\mathrm{H}' +
                          r'  \displaystyle = ' + sp.latex(hessian) + '$'))
        else:
            display(Latex(r'$ \displaystyle \text{Вещественных точек нет.} $'))

        df = pd.DataFrame(columns=['x', 'y', '|H|', 'z', 'types', 'color'])

        for i, dot in enumerate(relevant_points):
            h = hessian.subs(dot)
            display(Latex(r'$ \displaystyle \mathrm{H} \left(' +
                          r'  \displaystyle \mathrm{M}' + f'_{i + 1}' + r'\right) = ' + sp.latex(h) + '$'))
            h_det = h.det()
            dct = self.type_dot(h_det)

            df.loc[i] = [round(float(dot[x]), 4),
                         round(float(dot[y]), 4),
                         round(float(h_det), 4),
                         round(float(self.func.subs(dot)), 4),
                         dct['type'],
                         dct['color']]

        df = df.sort_values(['types', 'z'], ascending=[1, 0])

        plot = self.gen_plot(df)
        if df.shape[0] > 0:
            display(df)
            return df, plot

        else:
            return df, plot

    def min_max(self, points) -> None:
        """
        Если интервалы не задаются, то функция создает исходя из набора вещественных критических точек.
        Если они пустые, то интервал от -1, 1
        :param points: список точек из sympy solve, которые содержат ключи x, y - sm.symbols
        :return: None
        """
        if (self.interval_x is not None) and (np.inf not in self.interval_x) and (-np.inf not in self.interval_x) and \
           (self.interval_y is not None) and (np.inf not in self.interval_y) and (-np.inf not in self.interval_y):
            return

        x, y = self.variables
        if len(points) == 0:
            self.interval_x = [-1, 1]
            self.interval_y = [-1, 1]
            return

        min_x_y, max_x_y = [np.inf, np.inf], [-np.inf, -np.inf]

        for i, point in enumerate(points):
            min_x_y = [min(min_x_y[0], point[x]), min(min_x_y[1], point[y])]
            max_x_y = [max(max_x_y[0], point[x]), max(max_x_y[1], point[y])]

        min_x_y = [float(min_x_y[0] - 1), float(min_x_y[1] - 1)]
        max_x_y = [float(max_x_y[0] + 1), float(max_x_y[1] + 1)]

        if (self.interval_x is None) or (np.inf in self.interval_x) or (-np.inf in self.interval_x):
            self.interval_x = [min_x_y[0], max_x_y[0]]

        if (self.interval_y is None) or (np.inf in self.interval_y) or (-np.inf in self.interval_y):
            self.interval_y = [min_x_y[1], max_x_y[1]]

    def gen_plot(self, critical_points, path='graph'):

        surface_points = make_df_for_drawing(self.func, self.variables, self.interval_x, self.interval_y)
        rest_points = rest_func_points(self.func, self.g_func, self.variables, self.interval_x, self.interval_y)

        plot = draw_3d(surface_points, rest_points, critical_points)
        save_fig_to_pic(plot, path, ['html', 'png'])
        return plot


if __name__ == '__main__':
    x1, x2 = sp.symbols('x y')
    func1 = x1 ** 2 + x2 ** 2 - 25
    g_func1 = x1 + x2 - 1
    eq1 = LocalExtrWithRestrictions([x1, x2], func1, g_func1)
    sol1, plot1 = eq1.solve()

    func2 = x1 ** 2 - x2 ** 3 + 5
    g_func2 = (x1 - 1) ** 2 + x2 ** 3 + 1
    eq2 = LocalExtrWithRestrictions([x1, x2], func2, g_func2)
    sol2, plot2 = eq2.solve()

    func3 = x1 ** 2 - x2 ** 2 + 5
    g_func3 = (x1 - 1) ** 2 + x2 ** 2 - 1
    eq3 = LocalExtrWithRestrictions([x1, x2], func3, g_func3)
    sol3, plot3 = eq3.solve()
