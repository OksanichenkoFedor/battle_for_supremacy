import math

import pygame

from consts import WIDTH, HEIGHT, BORDER_COLOR, TEXT_COLOR, BORDER_WIDTH, BASE_HEX_COLOR, HEX_COLORS


class Hexagon:
    def __init__(self, q, r, id, size=40):
        self.q = q  # координата q (кубическая система координат)
        self.r = r  # координата r (кубическая система координат)
        self.id = id
        self.size = size
        self.color_id = -1
        self.calculate_pixel_position()
        self.is_team_base = False

    def calculate_pixel_position(self):
        """Переводит кубические координаты в пиксельные"""
        x = self.size * (math.sqrt(3) * self.q + math.sqrt(3) / 2 * self.r)
        y = self.size * (3 / 2 * self.r)
        self.x = x + WIDTH // 2
        self.y = y + HEIGHT // 2

    def get_vertices(self):
        """Возвращает вершины шестиугольника"""
        vertices = []
        for i in range(6):
            angle_deg = 60 * i + 30
            angle_rad = math.pi / 180 * angle_deg
            x = self.x + self.size * math.cos(angle_rad)
            y = self.y + self.size * math.sin(angle_rad)
            vertices.append((x, y))
        return vertices

    def draw(self, surface):
        """Рисует шестиугольник"""
        vertices = self.get_vertices()
        if self.color_id == -1:
            color = BASE_HEX_COLOR
        else:
            color = HEX_COLORS[self.color_id]

        pygame.draw.polygon(surface, color, vertices)
        pygame.draw.polygon(surface, BORDER_COLOR, vertices, BORDER_WIDTH)

        self.draw_coordinates(surface)

    def draw_coordinates(self, surface):
        """Рисует координаты q и r на шестиугольнике"""
        font = pygame.font.SysFont(None, 30)

        # Создаем текст с координатами
        coord_text = f"{self.id}"
        text_surface = font.render(coord_text, True, TEXT_COLOR)

        # Вычисляем позицию для текста (центр шестиугольника)
        text_rect = text_surface.get_rect(center=(self.x, self.y))

        # Рисуем текст
        surface.blit(text_surface, text_rect)

    def contains_point(self, point):
        """Проверяет, находится ли точка внутри шестиугольника"""
        x, y = point
        vertices = self.get_vertices()

        # Используем алгоритм проверки точки в полигоне
        n = len(vertices)
        inside = False
        p1x, p1y = vertices[0]
        for i in range(1, n + 1):
            p2x, p2y = vertices[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    def change_color(self, new_color_id):
        """Изменяет цвет шестиугольника"""
        self.color_id = new_color_id

    def reset_color(self):
        """Сбрасывает цвет к исходному"""
        self.color_id = -1