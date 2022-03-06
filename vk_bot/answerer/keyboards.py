from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class Keyboards:
    """
    Набор готовых клавиатур.
    """
    def __init__(self):
        self.keyboard = VkKeyboard(one_time=True, inline=False)

    def for_welcome(self) -> VkKeyboard:
        """
        Начальная клавиатура.

        Returns
        -------
        VkKeyboard
            Объект созданной клавиатуры.
        """

        self.keyboard.add_button('Меню', VkKeyboardColor.PRIMARY)
        self.keyboard.add_line()
        self.keyboard.add_button('Обо мне', VkKeyboardColor.SECONDARY)
        return self.keyboard

    def for_about_me(self) -> VkKeyboard:
        """
        Клавиатура для статуса about_me.

        Returns
        -------
        VkKeyboard
            Объект созданной клавиатуры.
        """

        self.keyboard.add_button('Меню', VkKeyboardColor.PRIMARY)
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
