import math

import pygame

from consts import BUTTON_CHOOSEN_WIDTH, BUTTON_UNCHOOSEN_WIDTH, BUTTON_UNCHOOSEN_COLOR, BUTTON_CHOOSEN_COLOR


class RadioButton:
    def __init__(self, x, y, size, color):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = color
        self.selected = False

    def draw(self, surface):
        # Рисуем круг для радио-кнопки (без фона)
        pygame.draw.circle(surface, self.color, self.rect.center, self.rect.width // 2)

        # Если кнопка выбрана, рисуем белую обводку
        if self.selected:
            pygame.draw.circle(surface, BUTTON_CHOOSEN_COLOR, self.rect.center,
                               self.rect.width // 2, BUTTON_CHOOSEN_WIDTH)  # Увеличили толщину обводки
        else:
            # Серая обводка для невыбранных кнопок
            pygame.draw.circle(surface, BUTTON_UNCHOOSEN_COLOR, self.rect.center,
                               self.rect.width // 2,  BUTTON_UNCHOOSEN_WIDTH)

    def is_clicked(self, pos):
        # Проверяем, находится ли точка внутри круга
        distance = math.sqrt((pos[0] - self.rect.centerx) ** 2 + (pos[1] - self.rect.centery) ** 2)
        return distance <= self.rect.width // 2