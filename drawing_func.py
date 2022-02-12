import pandas as pd
import plotly
import plotly.graph_objects as go
import numpy as np


def draw_3d(dots=None, critical_dots=None) -> go.Figure:
    """
    Функция рисует два графика и возвращает plotly Figure/
    Первый график 3-d поверхность, второй график - линия уровня

    Parameters
    ----------
    dots : DataFrame
        index is x, columns is y and values dots.loc[xi, yj] = f(xi, yj)

    critical_dots : list, array, DataFrame
        array with dots like (x, y, z)

    Returns
    -------
        plot

    Examples
    -------
    CNT_DOTS = 200

    dots = pd.DataFrame(index=np.linspace(-10, 10, CNT_DOTS),
                        columns=np.linspace(-1, 1, CNT_DOTS))

    for x in np.linspace(-10, 10, CNT_DOTS):
        for y in np.linspace(-1, 1, CNT_DOTS):
            dots.loc[x, y] = f(x, y)
    draw_3d(dots)
    """

    fig = plotly.subplots.make_subplots(rows=1, cols=2,
                                        specs=[[{'is_3d': True}, {'is_3d': False}]],
                                        subplot_titles=['График функции', 'Линии уровня'])

    fig.add_trace(go.Surface(x=dots.index, y=dots.columns, z=dots.values, opacity=0.7), 1, 1)

    fig.add_trace(go.Contour(x=dots.index, y=dots.columns, z=dots.values, opacity=0.7,
                             contours={'start': min(dots.values.flatten()),
                                       'end': max(dots.values.flatten()),
                                       'size': 2},
                             colorscale='ice'), 1, 2)
    return fig


def make_df_for_drawing(func, x_constraints:[tuple], y_constraints:[tuple]) -> pd.DataFrame:
    """

    :param func: function for drawing
    :param x_constraints: tuple, like (-10, 10). x is in (-10, 10)
    :param y_constraints: tuple for y
    :return: pd.DataFrame with applying func for each pair of cartesian product x and y
    """

    pass