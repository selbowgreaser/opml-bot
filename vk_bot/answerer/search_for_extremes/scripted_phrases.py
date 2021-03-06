from typing import NamedTuple

from solver_core.search_for_extremes.handlers.operations_name_gen import allowed_operations


class Phrases(NamedTuple):
    TASK_TYPE_SELECTION = 'Давай найдем экстремум твоей функции.\n\n ' \
                          'Если в твоем условии есть ограничивающая функция, то жми кнопку "С ограничивающей ' \
                          'функцией"\n\n' \
                          'Выбери тип задачи:'
    CLICK_BUTTON = 'Не понял... Нажми на клавиатуру ☝🏻'
    INPUT_VARS = 'Теперь тебе нужно ввести входные данные отдельными сообщениями.\n\n' \
                 'Начни с имен переменных. Они не могут начинаться с цифры,' \
                 'а также содержать что-то кроме латинских букв и цифр.\n\n' \
                 'Пример: x y'
    INPUT_FUNC = 'Отлично!\n\n' \
                 f'Теперь введи функцию. Доступные имена: {", ".join(allowed_operations)}\n\n' \
                 'Пример: x**2 + 0.5 * y**2'
    INPUT_G_FUNC = 'Все в порядке.\n\n' \
                   'Введи ограничивающую функцию.\n\n' \
                   'Пример: x**3 + y**3 - 1'
    INPUT_RESTR = 'Ограничивающая функция добавлена.\n\n' \
                  'Есть ли у твоей функции ограничения?'
    INPUT_INTERVAL_X = 'Введи ограничения по оси X через пробел. Если ограничений по оси нет, введи слово None.' \
                       'Для обозначения бесконечностей используй -oo или +oo (маленькая английская буква О).\n\n' \
                       'Пример: -oo 100'
    INPUT_INTERVAL_Y = 'Теперь то же самое, но для оси Y.' \
                       'Пример: -5 5'
    COMPUTE = 'Нажми кнопку и жди результата! :)'
    LINK = '\n\nПосмотреть на график -> https://opml-bot.herokuapp.com/'
    ERROR = 'При обработке данных произошла ошибка: {}'
