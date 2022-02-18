import pandas as pd
import plotly
import plotly.graph_objects as go
import numpy as np

GRID_WIDTH = 1


def draw_3d(dots: [pd.DataFrame], critical_dots: [list, None] = None) -> go.Figure:
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

    f = lambda x, y: x ** 2 + y ** 2

    dots = pd.DataFrame(index=np.linspace(-10, 10, CNT_DOTS),
                        columns=np.linspace(-10, 10, CNT_DOTS))

    for x in np.linspace(-10, 10, CNT_DOTS):
        for y in np.linspace(-10, 10, CNT_DOTS):
            dots.loc[x, y] = f(x, y)

    draw_3d(dots, [(0, 0, 0), (1, 0, 1), (0, 1, 1)])
    """
    min_value = min(dots.values.flatten())
    max_value = max(dots.values.flatten())

    fig = plotly.subplots.make_subplots(rows=1, cols=2,
                                        specs=[[{'is_3d': True}, {'is_3d': False}]],
                                        subplot_titles=['График функции', 'Линии уровня'])

    fig.add_trace(go.Surface(x=dots.index,
                             y=dots.columns,
                             z=dots.values,
                             opacity=0.5,
                             showscale=False,
                             colorscale='ice'), 1, 1)

    fig.update_scenes(xaxis_title_text='x, у.е.',
                      yaxis_title_text='y, у.е.',
                      zaxis_title_text='z, у.е.')

    fig.update_xaxes(title='x, у.е.', col=2, row=1, gridwidth=GRID_WIDTH, gridcolor='black',
                     zerolinecolor='black', zerolinewidth=GRID_WIDTH)
    fig.update_yaxes(title='y, у.е.', col=2, row=1, gridwidth=GRID_WIDTH, gridcolor='black',
                     zerolinecolor='black', zerolinewidth=GRID_WIDTH)

    fig.add_trace(go.Contour(x=dots.index,
                             y=dots.columns,
                             z=dots.values,
                             opacity=0.75,
                             contours={
                                 'start': min_value,
                                 'end': max_value,
                                 'size': (max_value - min_value) // 15,
                                 # 'showlabels':True,
                                 # 'labelfont':dict(size = 8, color = 'white')
                             },
                             colorscale='ice'), 1, 2)

    if critical_dots is not None:
        critical_dots = np.array(critical_dots)
        fig.add_scatter3d(x=critical_dots[:, 0],
                          y=critical_dots[:, 1],
                          z=critical_dots[:, 2],
                          mode='markers',
                          marker=dict(size=6, color='red'),
                          showlegend=False,
                          name='critical dots')

        fig.add_scatter(x=critical_dots[:, 0],
                        y=critical_dots[:, 1],
                        mode='markers',
                        marker=dict(size=10, color='red'),
                        showlegend=False,
                        name='critical dots')

    return fig


def make_df_for_drawing(func, x_constraints: [tuple], y_constraints: [tuple], cnt_dots=50) -> pd.DataFrame:
    """
    Calculate the function for each pair of coordinates from the Cartesian product
    of x_constraints and y_constraints.
    :param func: function for drawing
    :param x_constraints: tuple, like (-10, 10). x is in (-10, 10)
    :param y_constraints: tuple for y
    :param cnt_dots: number of points on each axis
    :return: pd.DataFrame with applying func for each pair of cartesian product x and y
    """

    dots = pd.DataFrame(index=np.linspace(x_constraints[0], x_constraints[1], cnt_dots),
                        columns=np.linspace(y_constraints[0], y_constraints[1], cnt_dots))

    for x in np.linspace(x_constraints[0], x_constraints[1], cnt_dots):
        for y in np.linspace(y_constraints[0], y_constraints[1], cnt_dots):
            dots.loc[x, y] = func(x, y)

    return dots


def save_fig_to_pic(fig: go.Figure, path: str, extensions: list) -> None:
    """
    Save fig in image requested formats
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
        fig.write_image(path + '.' + extension, width=2048, height=1024,)
