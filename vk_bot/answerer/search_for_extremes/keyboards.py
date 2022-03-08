from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class Keyboards:
    """
    Набор готовых клавиатур.
    """
    def __init__(self):
        self.keyboard = VkKeyboard(one_time=True, inline=False)

    def for_task_type_selection(self) -> VkKeyboard:
        """
        Выбор типа задачи.

        Returns
        -------
        VkKeyboard
            Объект созданной клавиатуры.
        """

        self.keyboard.add_button('Обычная', VkKeyboardColor.PRIMARY)
        self.keyboard.add_button('С ограничивающей функцией', VkKeyboardColor.SECONDARY)
        return self.keyboard

    def for_input_restr(self):
        """
        Наличие или отсутствие ограничений.

        Returns
        -------
        VkKeyboard
            Объект созданной клавиатуры.
        """
        self.keyboard.add_button("Да", VkKeyboardColor.POSITIVE)
        self.keyboard.add_button("Нет", VkKeyboardColor.NEGATIVE)
        return self.keyboard

    def for_menu(self) -> VkKeyboard:
        """
        Клавиатура для статуса menu.

        Returns
        -------
        VkKeyboard
            Объект созданной клавиатуры.
        """

        self.keyboard.add_button('Поиск экстремума', VkKeyboardColor.POSITIVE)
        self.keyboard.add_line()
        self.keyboard.add_button('Обо мне', VkKeyboardColor.SECONDARY)
        return self.keyboard

    def for_compute(self):
        """
        Клавиатура для старта вычислений.

        Returns
        -------
        VkKeyboard
            Объект созданной клавиатуры.
        """

        self.keyboard.add_button('Вычислить', VkKeyboardColor.POSITIVE)
        return self.keyboard
