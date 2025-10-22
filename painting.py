import pygame

from consts import WIDTH, TEXT_COLOR, HEX_COLORS, BASE_HEX_COLOR, BUTTON_SIZE, BUTTON_X, BUTTON_Y, BUTTON_SPACING
from radiobutton import RadioButton


class Painting:
    def __init__(self, screen):
        self.screen = screen
        self.current_color_id = 0
        self.create_radio_buttons()

    def create_radio_buttons(self):
        """Создает радио-кнопки для выбора цвета"""
        self.buttons = []

        for i, color in enumerate(HEX_COLORS):
            button = RadioButton(
                BUTTON_X,
                BUTTON_Y + i * BUTTON_SPACING,
                BUTTON_SIZE,
                color
            )
            self.buttons.append(button)

        # Первая кнопка выбрана по умолчанию
        self.buttons[0].selected = True
        button = RadioButton(
            BUTTON_X,
            BUTTON_Y + len(HEX_COLORS) * BUTTON_SPACING,
            BUTTON_SIZE,
            BASE_HEX_COLOR
        )
        self.buttons.append(button)

    def is_clicked(self, mouse_pos):
        for i, button in enumerate(self.buttons):
            if button.is_clicked(mouse_pos):
                return i
        return -1

    def parce_clicking(self, id_selected):
        for btn in self.buttons:
            btn.selected = False

        self.buttons[id_selected].selected = True
        self.current_color_id = id_selected

    def get_current_color_id(self):
        if self.current_color_id==len(HEX_COLORS):
            return -1
        return self.current_color_id

    def draw(self):
        font = pygame.font.SysFont(None, 36)
        title_text = "Цвета"
        title_surface = font.render(title_text, True, BASE_HEX_COLOR)
        self.screen.blit(title_surface, (WIDTH - 140, 30))

        # Рисуем радио-кнопки
        for button in self.buttons:
            button.draw(self.screen)
