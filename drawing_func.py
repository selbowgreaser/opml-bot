import pandas as pd
import plotly
import plotly.graph_objects as go
import numpy as np
import sympy as sp

np.seterr('ignore')

GRID_WIDTH = 1


def draw_3d(points_of_function: pd.DataFrame,
            points_of_restriction: pd.DataFrame = None,
            critical_points: pd.DataFrame = None) -> go.Figure:
    """
    Функция рисует два графика и возвращает plotly Figure. Первый график 3-d поверхность, второй график - линии уровня.
    На первом и втором графиках рисуются точки critical_points и ограничивающая функция.

    Code examples::

        import sympy as sp

        x, y = sp.symbols('x y')
        func = x ** 2 - y ** 2 / 2
        restr_func = x + y
        x_constr = (-2, 2)
        y_constr = (-2, 2)

        data = make_df_for_drawing(func, [x, y], x_conts, y_conts, 39)

        points = pd.DataFrame({'x':[0, 1],
                               'y':[0, 1],
                               'z':[0, 2],
                               'types':['saddle', 'Пример точки'],
                               'color':['yellow', 'red']})


        rest_points = rest_func_points(func, restr_func, [x, y], x_constr, y_constr)
        fig = draw_3d(data, rest_points, points)
        fig.show()

        # Интересная поверхность и ограничения - окружность
        x, y = sp.symbols('x y')
        func = (x + y) ** 2 + y * sp.cos(2 * x * sp.pi) + x * sp.sin(2 * y * sp.pi)
        restr_func = x ** 2  + y ** 2 - 9
        x_constr = (-5, 3.5)
        y_constr = (-4, 3)

        data = make_df_for_drawing(func, [x, y], x_constr, y_constr, 39)
        rest_points = rest_func_points(func, restr_func, [x, y], x_constr, y_constr)
        fig = draw_3d(data, rest_points)

        fig.show()

    :param points_of_function: Датафрейм, у которого индексы - это значения по оси x,
                               столбцы - значения по оси y, сами значения функции это матрица df.values.
    :param points_of_restriction: Датафрейм с тремя столбцами x, y, z для ограничивающей функции
    :param critical_points: Датафрейм, который содержить столбцы x, y, z, type, color для каждой
                            критической точки.
    :return: go.Figure. Фигуру в plotly, с двумя подграфиками.


    """

    if not isinstance(points_of_function, pd.DataFrame):
        raise TypeError('Массив dots не является pd.DataFrame')

    min_value = min(filter(np.isfinite, points_of_function.values.flatten()))
    max_value = max(filter(np.isfinite, points_of_function.values.flatten()))

    fig = plotly.subplots.make_subplots(rows=1, cols=2,
                                        specs=[[{'is_3d': True}, {'is_3d': False}]],
                                        subplot_titles=['График функции', 'Линии уровня'])

    fig.add_trace(go.Surface(x=points_of_function.index,
                             y=points_of_function.columns,
                             z=points_of_function.values.T,
                             opacity=0.5,
                             showscale=False,
                             colorscale='ice',
                             name='f(x, y)'),
                  row=1,
                  col=1)

    fig.update_scenes(xaxis_title_text='x, у.е.',
                      yaxis_title_text='y, у.е.',
                      zaxis_title_text='z, у.е.')

    fig.update_xaxes(title='x, у.е.', col=2, row=1, gridwidth=GRID_WIDTH, gridcolor='black',
                     zerolinecolor='black', zerolinewidth=GRID_WIDTH)
    fig.update_yaxes(title='y, у.е.', col=2, row=1, gridwidth=GRID_WIDTH, gridcolor='black',
                     zerolinecolor='black', zerolinewidth=GRID_WIDTH)

    fig.add_trace(go.Contour(x=points_of_function.index,
                             y=points_of_function.columns,
                             z=points_of_function.values.T,
                             opacity=0.75,
                             contours={
                                 'start': min_value,
                                 'end': max_value,
                                 'size': (max_value - min_value) // 15,
                             },
                             colorscale='ice',
                             name='f(x, y)'),
                  row=1,
                  col=2)

    if critical_points is not None and len(critical_points) > 0:

        for type_point, points_of_function in critical_points.groupby('types'):
            fig.add_scatter3d(x=points_of_function.x,
                              y=points_of_function.y,
                              z=points_of_function.z,
                              mode='markers',
                              marker=dict(size=6, color=points_of_function.color),
                              showlegend=True,
                              name=type_point
                              )

            fig.add_scatter(x=points_of_function.x,
                            y=points_of_function.y,
                            customdata=points_of_function.z,
                            hovertemplate='x: %{x}<br><extra></extra>' +
                                          'y: %{y}<br>' +
                                          'z: %{customdata}<br>',
                            mode='markers',
                            marker=dict(size=10, color=points_of_function.color),
                            showlegend=False,
                            name=type_point
                            )

    fig.update_layout(legend=dict(yanchor="top",
                                  y=1,
                                  xanchor="left",
                                  x=-0.2
                                  ))

    if isinstance(points_of_restriction, pd.DataFrame):
        line3d = go.Scatter3d(x=points_of_restriction.x,
                              y=points_of_restriction.y,
                              z=points_of_restriction.z,
                              mode='lines',
                              line={'width': 3, 'color': 'darkblue'},
                              name='g(x, y) 3d')
        fig.add_trace(line3d, row=1, col=1)

        line = go.Scatter(x=points_of_restriction.x,
                          y=points_of_restriction.y,
                          customdata=points_of_restriction.z.round(7),
                          hovertemplate='x: %{x}<br>' +
                                        'y: %{y}<br>' +
                                        'z: %{customdata}<extra></extra>',
                          mode='lines',
                          line={'width': 2, 'color': 'darkblue'},
                          name='g(x, y)')

        fig.add_trace(line, row=1, col=2)

    return fig


def make_df_for_drawing(func,
                        variables,
                        x_constraints: tuple,
                        y_constraints: tuple,
                        cnt_points: int = 49) -> pd.DataFrame:
    """
    Создает данные для отрисовки основной функции. Можно передать передать функцию как функцию, зависимую от двух
    аргументов или как sympy выражение. Если вы передаете sympy выражение, то обязательно передайте variables

    :param func: Функция, которую нужно отрисовать
    :param variables: список и кортеж переменных в функции func
    :param x_constraints: ограничения по оси x
    :param y_constraints: ограничения по оси y
    :param cnt_points: количество точек на каждой оси. Всего получиться cnt_points ** 2 точек.

    :return: Датафрейм с точками для отрисовки в draw_3d.
    Code examples::

        import sympy as sp

        x, y = sp.symbols('x y')
        func = x ** 2 - y ** 2 / 2
        restr_func = x + y

        data = make_df_for_drawing(func, [x, y], (-2, 2), (-2, 2), 39)
    """

    func = sp.lambdify(variables, func)

    x_axis = np.linspace(x_constraints[0], x_constraints[1], cnt_points)
    y_axis = np.linspace(y_constraints[0], y_constraints[1], cnt_points)

    points = pd.DataFrame(index=x_axis,
                          columns=y_axis)

    x_axis = list(x_axis)
    y_axis = list(y_axis)

    for x_i in x_axis:
        for y_i in y_axis:
            f = func(x_i, y_i)
            if np.isfinite(f):
                points.loc[x_i, y_i] = f
            else:
                points.loc[x_i, y_i] = np.nan

    return points


def save_fig_to_pic(fig: go.Figure, path: str, extensions: list) -> None:
    """
    Сохраняет график в нужных форматах

    :param fig: какой plotly график нужно сохранить
    :param path: путь с названием файла для сохранения без расширения
    :param extensions: список расширений
    :return: None

    Code examples::

        save_fig_to_pic(fig, 'plot_3d', ['png', 'jpeg', 'html'])

    """

    if 'html' in extensions:
        fig.write_html(path + '.html', default_width=1336, default_height=668)
        extensions.remove('html')

    for extension in extensions:
        fig.write_image(path + '.' + extension, width=2048, height=1024, )


def rest_func_points(func,
                     restr_func,
                     variables,
                     x_const: tuple,
                     y_const: tuple,
                     cnt_points: int = 40) -> pd.DataFrame:
    """
    Создает данные для отрисовки ограничивающей функции
    ФУНКЦИИ ДОЛЖНЫ БЫТЬ sympy выражениями

    Code examples::

        import sympy as sp
        x, y = sp.symbols('x y')
        func = x ** 2 - y ** 2 / 2
        restr_func = x + y
        rest_points = rest_func_points(func, restr_func, [x, y], (-2, 2), (-2, 2))

    :param func: Функция, поверхность, которой построена
    :param restr_func: Ограничивающая функция
    :param variables: Список с переменными
    :param x_const: Ограничения по оси x
    :param y_const: Ограничения по оси y
    :param cnt_points: Количество точек на каждой оси. АККУРАТНО, долго будет работать код на больших значениях
    :return: pd.DataFrame с точками для отрисовки. Столбцы x, y, z


    """

    real_variables = sp.symbols('x y', real=True)
    func = func.subs(dict(zip(variables, real_variables)))
    restr_func = restr_func.subs(dict(zip(variables, real_variables)))
    epsilon_x = (x_const[1] - x_const[0]) / cnt_points
    epsilon_y = (y_const[1] - y_const[0]) / cnt_points

    x, y = real_variables

    out_df = pd.DataFrame(columns=['x', 'y', 'z'])

    i = 0
    for y_i in np.linspace(y_const[0], y_const[1], cnt_points):
        try:
            x_solve = sp.solve(restr_func.subs({y: y_i}), [x])
        except NotImplementedError:
            try:
                x_solve = [sp.nsolve(restr_func.subs({y: y_i}), x, x_const[0])]
            except ValueError:
                x_solve = []

        for x_i in x_solve:
            x_i = float(x_i)
            if x_const[0] <= x_i <= x_const[1]:
                out_df.loc[i] = [x_i, y_i, float(func.subs({x: x_i, y: y_i}))]
                i += 1

    for x_i in np.linspace(x_const[0], x_const[1], cnt_points):
        try:
            y_solve = sp.solve(restr_func.subs({x: x_i}), [y])
        except NotImplementedError:
            try:
                y_solve = [sp.nsolve(restr_func.subs({x: x_i}), [y], y_const[0])]
            except ValueError:
                y_solve = []

        for y_i in y_solve:
            y_i = float(y_i)
            if y_const[0] <= y_i <= y_const[1]:
                out_df.loc[i] = [x_i, y_i, float(func.subs({x: x_i, y: y_i}))]
                i += 1

    out_df = out_df.sort_values('x').reset_index(drop=True)

    len_ways = pd.DataFrame(index=out_df.index,
                            columns=out_df.index)

    for i, dot1 in enumerate(out_df[['x', 'y']].apply(tuple, axis=1)):
        for j, dot2 in enumerate(out_df[['x', 'y']].apply(tuple, axis=1)):
            if i == j:
                len_ways.iloc[i, j] = np.inf
            else:
                len_ways.iloc[i, j] = (dot1[0] - dot2[0]) ** 2 + (dot1[1] - dot2[1]) ** 2

    len_ways = len_ways.astype(float)
    way = [0]
    for i in range(len_ways.shape[0] - 1):
        source = way[-1]
        target, length = len_ways.loc[source].idxmin(), len_ways.loc[source].min()
        len_ways.loc[source] = np.inf
        len_ways.loc[:, source] = np.inf
        if length > (epsilon_x + epsilon_y):
            break
        way.append(target)

    if check_dot_in_round(out_df.loc[way[0], ['x', 'y']].values,
                          out_df.loc[way[-1], ['x', 'y']].values,
                          epsilon_x,
                          epsilon_y):
        way.append(0)

    return out_df.loc[way]


def check_dot_in_round(center, check_point, radius_x, radius_y) -> bool:
    """
    Вспомогательная функция для rest_func_points
    Проверяет, входит ли точка check_point в малую окрестность точки center
    :param center: Основная точка, окрестность которой рассматриваем
    :param check_point: Точка, которую проверяем
    :param radius_x: значение по оси x
    :param radius_y: значение по оси y
    :return: False - точка не входит, True - точка входит
    """
    flag_x = False
    if center[0] - radius_x <= check_point[0] <= center[0] + radius_x:
        flag_x = True

    flag_y = False
    if center[1] - radius_y <= check_point[1] <= center[1] + radius_y:
        flag_y = True

    return flag_x * flag_y
