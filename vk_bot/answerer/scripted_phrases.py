from typing import NamedTuple


class Phrases(NamedTuple):
    GREETINGS = 'Привет, {}!'
    ABOUT_ME = 'Я бот с кодовым названием OPML.\n\nМоей разработкой занималась команда из шести студентов Финансового ' \
               'университета. Давай я познакомлю тебя с ними:\n\n' \
               '*alxndr.andrvch(Александр Фролов) – Project Manager, Tech Lead\n' \
               '*id245919670(Алина Шаркова) – Analyst\n' \
               '*mashaplastinina(Мария Пластинина) – Analyst\n' \
               '*vktrbr(Виктор Барбарич) – Programmer\n' \
               '*gospod_bogg(Виталий Тимофеев) – Programmer\n' \
               '*0nadya(Надежда Гераськина) – Tester\n\n' \
               'Если хочешь лучше узнать мой внутренний мир, тебе сюда -> https://github.com/selbowgreaser/opml_bot\n'
    MENU = 'Выбери то, что тебе нужно:'
    CLICK_BUTTON = 'Не понял... Нажми на клавиатуру ☝🏻'
