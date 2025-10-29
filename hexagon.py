import math
import random

import pygame

from consts import WIDTH, HEIGHT, BORDER_COLOR, TEXT_COLOR, BORDER_WIDTH, BASE_HEX_COLOR, HEX_COLORS, STAR_COLOR, \
    SPARKLE_COLOR, HEX_SIZE


class Hexagon:
    def __init__(self, q, r, id, size=HEX_SIZE, is_star=False):
        self.q = q  # координата q (кубическая система координат)
        self.r = r  # координата r (кубическая система координат)
        self.id = id
        self.size = size
        self.color_id = -1
        self.calculate_pixel_position()
        self.is_team_base = False
        self.is_star = is_star

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

    def draw_star(self, surface):
        """Рисует звезду с блестками"""

        star_radius = self.size * 0.6  # Размер звезды

        # Рисуем основную звезду (5 лучей)
        points = []
        for i in range(10):
            angle = math.pi / 2 + i * math.pi / 5
            radius = star_radius if i % 2 == 0 else star_radius * 0.4
            x = self.x + radius * math.cos(angle)
            y = self.y + radius * math.sin(angle)
            points.append((x, y))

        pygame.draw.polygon(surface, STAR_COLOR, points)

        # Добавляем блестки (маленькие кружки вокруг звезды)
        for i in range(8):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(star_radius * 0.7, star_radius * 1.2)
            sparkle_x = self.x + distance * math.cos(angle)
            sparkle_y = self.y + distance * math.sin(angle)
            sparkle_radius = random.uniform(1, 3)
            pygame.draw.circle(surface, SPARKLE_COLOR, (int(sparkle_x), int(sparkle_y)), sparkle_radius)

        # Добавляем внутреннее свечение
        for i in range(3):
            glow_radius = star_radius * (0.3 + i * 0.2)
            glow_surface = pygame.Surface((int(glow_radius * 2), int(glow_radius * 2)), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (*STAR_COLOR, 50), (int(glow_radius), int(glow_radius)), int(glow_radius))
            surface.blit(glow_surface, (self.x - glow_radius, self.y - glow_radius),
                         special_flags=pygame.BLEND_ALPHA_SDL2)

    def draw(self, surface):
        """Рисует шестиугольник"""
        vertices = self.get_vertices()
        if self.color_id == -1:
            color = BASE_HEX_COLOR
        else:
            color = HEX_COLORS[self.color_id]

        pygame.draw.polygon(surface, color, vertices)
        pygame.draw.polygon(surface, BORDER_COLOR, vertices, BORDER_WIDTH)

        if self.is_star:
            self.draw_star(surface)
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


def hex_pixel_distance(hex1, hex2):
    # Вычисляем пиксельные координаты центров
    if hex1.size!=hex2.size:
        raise Exception("different hexes")
    hex_size = hex1.size
    x1 = hex_size * (math.sqrt(3) * hex1.q + math.sqrt(3) / 2 * hex1.r)
    y1 = hex_size * (3 / 2 * hex1.r)

    x2 = hex_size * (math.sqrt(3) * hex2.q + math.sqrt(3) / 2 * hex2.r)
    y2 = hex_size * (3 / 2 * hex2.r)

    # Евклидово расстояние
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    return distance