import pygame

from consts import LOAD_BUTTON_COLOR, LOAD_BUTTON_TEXT_COLOR


class LoadButton:
    def __init__(self, x, y, width, height, text, field, screen, color=LOAD_BUTTON_COLOR, text_color=LOAD_BUTTON_TEXT_COLOR):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.field = field
        self.field.load_button = self
        self.screen = screen
        self.text_color = text_color
        self.font = pygame.font.SysFont(None, 32)

    def draw(self):
        # Рисуем прямоугольник кнопки
        pygame.draw.rect(self.screen, self.color, self.rect)
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 2)  # Черная обводка

        # Рисуем текст
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        if self.rect.collidepoint(pos):
            self.field.load()
            return True
        return False



