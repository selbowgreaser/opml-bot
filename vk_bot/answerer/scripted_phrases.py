from typing import NamedTuple


class Phrases(NamedTuple):
    greetings = 'Привет, {}!'
    about_me = 'Я бот с кодовым названием OPML.\n\nМоей разработкой занималась команда из шести студентов Финансового' \
               'университета. Давай я познакомлю тебя с ними:\n\n' \
               '*alxndr.andrvch(Александр Фролов) – Project Manager\n' \
               '*id245919670(Алина Шаркова) – Analyst\n' \
               '*mashaplastinina(Мария Пластинина) – Analyst\n' \
               '*vktrbr(Виктор Барбарич) – Programmer\n' \
               '*gospod_bogg(Виталий Тимофеев) – Programmer\n' \
               '*0nadya(Надежда Гераськина) – Tester\n\n' \
               'Если хочешь лучше узнать мой внутренний мир, тебе сюда -> https://github.com/selbowgreaser/opml_1\n'
    click_button = 'Не понял... Нажми на клавиатуру ☝🏻'
