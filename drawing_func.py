import pandas as pd
import plotly
import plotly.graph_objects as go
import numpy as np
import sympy as sp

np.seterr('ignore')

GRID_WIDTH = 1


def draw_3d(points: pd.DataFrame,
            rest_func_points: pd.DataFrame = None,
            critical_points: pd.DataFrame = None) -> go.Figure:
    """
    ----------
        Функция рисует два графика и возвращает plotly Figure.
        Первый график 3-d поверхность, второй график - линия уровня

    Parameters
    ----------
        points : pd.DataFrame. Датафрейм, у которого индексы - это значения по оси x,
                 столбцы - значения по оси y, сами значения функции это матрица values.
        rest_func_points : pd.DataFrame с тремя столбцами x, y, z
        critical_points : pd.DataFrame, который обязательно содержит столбцы x, y, z, types
    Returns
    ----------
        go.Figure
    Examples
    ----------
        import sympy as sp

        x, y = sp.symbols('x y')
        func = x ** 2 - y ** 2 / 2
        restr_func = x + y
        x_conts = (-2, 2)
        y_conts = (-2, 2)

        data = make_df_for_drawing(func, [x, y], x_conts, y_conts, 39)

        points = pd.DataFrame({'x':[0, 1],
                               'y':[0, 1],
                               'z':[0, 2],
                               'types':['saddle', 'Пример точки'],
                               'color':['yellow', 'red']})


        rest_points = rest_func_points(func, restr_func, [x, y], x_conts, y_conts)
        fig = draw_3d(data, rest_points, points)
        fig

    """
    if not isinstance(points, pd.DataFrame):
        raise TypeError('Массив dots не является pd.DataFrame')

    min_value = min(filter(np.isfinite, points.values.flatten()))
    max_value = max(filter(np.isfinite, points.values.flatten()))

    fig = plotly.subplots.make_subplots(rows=1, cols=2,
                                        specs=[[{'is_3d': True}, {'is_3d': False}]],
                                        subplot_titles=['График функции', 'Линии уровня'])

    fig.add_trace(go.Surface(x=points.index,
                             y=points.columns,
                             z=points.values.T,
                             opacity=0.5,
                             showscale=False,
                             colorscale='ice'),
                  row=1,
                  col=1)

    fig.update_scenes(xaxis_title_text='x, у.е.',
                      yaxis_title_text='y, у.е.',
                      zaxis_title_text='z, у.е.')

    fig.update_xaxes(title='x, у.е.', col=2, row=1, gridwidth=GRID_WIDTH, gridcolor='black',
                     zerolinecolor='black', zerolinewidth=GRID_WIDTH)
    fig.update_yaxes(title='y, у.е.', col=2, row=1, gridwidth=GRID_WIDTH, gridcolor='black',
                     zerolinecolor='black', zerolinewidth=GRID_WIDTH)

    fig.add_trace(go.Contour(x=points.index,
                             y=points.columns,
                             z=points.values.T,
                             opacity=0.75,
                             contours=
                             {
                                 'start': min_value,
                                 'end': max_value,
                                 'size': (max_value - min_value) // 15,
                             },
                             colorscale='ice'),
                  row=1,
                  col=2)

    if critical_points is not None and len(critical_points) > 0:

        for type_point, points in critical_points.groupby('types'):
            fig.add_scatter3d(x=points.x,
                              y=points.y,
                              z=points.z,
                              mode='markers',
                              marker=dict(size=6, color=points.color),
                              showlegend=True,
                              name=type_point
                              )

            fig.add_scatter(x=points.x,
                            y=points.y,
                            customdata=points.z,
                            hovertemplate='x: %{x}<br><extra></extra>' + \
                                          'y: %{y}<br>' + \
                                          'z: %{customdata}<br>',
                            mode='markers',
                            marker=dict(size=10, color=points.color),
                            showlegend=False,
                            name=type_point
                            )

    fig.update_layout(legend=dict(yanchor="top",
                                  y=1,
                                  xanchor="left",
                                  x=-0.2
                                  ))

    if isinstance(rest_func_points, pd.DataFrame):
        line = go.Scatter3d(x=rest_func_points.x,
                            y=rest_func_points.y,
                            z=rest_func_points.z,
                            mode='lines',
                            line={'width': 2, 'color': 'darkblue'},
                            name='g(x, y)')
        fig.add_trace(line, row=1, col=1)
    return fig


def make_df_for_drawing(func,
                        variables,
                        x_constraints: tuple,
                        y_constraints: tuple,
                        cnt_points: int = 50) -> pd.DataFrame:
    """
        Calculate the function for each pair of coordinates from the Cartesian product
        of x_constraints and y_constraints.
    Args
    ------
        func: function for drawing. Sympy expression
        variables: Переменные, которые используются в функции
        x_constraints: tuple, like (-10, 10). x is in (-10, 10)
        y_constraints: tuple for y
        cnt_points: number of points on each axis

    Returns
    ------
        pd.DataFrame with applying func for each pair of cartesian product x and y
    """

    func = sp.lambdify(variables, func)

    x_axis = np.linspace(x_constraints[0], x_constraints[1], cnt_points)
    y_axis = np.linspace(y_constraints[0], y_constraints[1], cnt_points)

    points = pd.DataFrame(index=x_axis,
                          columns=y_axis)

    x_axis = list(x_axis)
    y_axis = list(y_axis)

    for x in x_axis:
        for y in y_axis:
            f = func(x, y)
            if np.isfinite(f):
                points.loc[x, y] = f
            else:
                points.loc[x, y] = np.nan

    return points


def save_fig_to_pic(fig: go.Figure, path: str, extensions: list) -> None:
    """
        Save fig in image requested formats
    Args:
    -----
        :param fig: the Figure to be saved
        :param path: path without filename extension
        :param extensions: formats - list of formats
    Examples
    ------
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
                     y_const: tuple) -> pd.DataFrame:

    """
    ------
        Создает данные для отрисовки ограничивающей функции
        ФУНКЦИИ ДОЛЖНЫ БЫТЬ sympy выражениями
    Args
    ------
        func: Функция, поверхность, которой построена
        restr_func: Ограничивающая функция

    :Return:
    ------
        pd.DataFrame с точками для отрисовки. Столбцы x, y, z
    """
    x, y = variables

    out_df = pd.DataFrame(columns=['x', 'y', 'z'])
    i = 0
    for x_i in np.linspace(x_const[0], x_const[1], 99):
        y_solve = sp.solve(restr_func.subs({x: x_i}), [y])
        for y_i in y_solve:
            y_i = float(y_i)
            if y_const[0] < y_i < y_const[1]:
                out_df.loc[i] = [x_i, y_i, float(func.subs({x: x_i, y: y_i}))]
                i += 1
    return out_df


if __name__ == '__main__':
    import sympy as sp

    x, y = sp.symbols('x y')
    func = x ** 2 - y ** 2 / 2
    restr_func = x + y
    x_conts = (-2, 2)
    y_conts = (-2, 2)

    data = make_df_for_drawing(func, [x, y], x_conts, y_conts, 39)

    points = pd.DataFrame({'x': [0, 1],
                           'y': [0, 1],
                           'z': [0, 2],
                           'types': ['saddle', 'Пример точки'],
                           'color': ['yellow', 'red']})

    rest_points = rest_func_points(func, restr_func, [x, y], x_conts, y_conts)
    fig = draw_3d(data, rest_points, points)
    save_fig_to_pic(fig, 'figure', ['html'])