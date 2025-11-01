import math
import time

import pygame

from consts import ANIMATION_SPEED, HEX_COLORS


def draw_line(surface, line_start, line_end, line_color_id):
    # Рисуем основную линию тонкой пунктирной линией
    pygame.draw.line(surface, HEX_COLORS[line_color_id], line_start, line_end, 1)

    # Вычисляем вектор направления
    dx = line_end[0] - line_start[0]
    dy = line_end[1] - line_start[1]
    length = math.sqrt(dx * dx + dy * dy)

    if length > 0:  # Избегаем деления на ноль
        # Нормализуем вектор
        dx /= length
        dy /= length

        # Количество треугольников (зависит от длины линии)
        num_triangles = max(3, int(length / 25))

        current_time = time.time()
        phase = (current_time * ANIMATION_SPEED / (1.0*length)) % 1.0  # Фаза от 0 до 1

        # Фиксированный размер треугольника (максимальный из предыдущего кода)
        triangle_size = 15  # 8 + 4 = 12 (максимальный размер из предыдущего кода)

        # Фиксированный цвет треугольника (золотой)
        triangle_color = HEX_COLORS[line_color_id]  # Золотой цвет

        for i in range(num_triangles):
            # Позиция треугольника с анимацией
            t = (i / num_triangles + phase) % 1.0
            pos_x = line_start[0] + dx * length * t
            pos_y = line_start[1] + dy * length * t

            # Вершины треугольника (направлен вдоль линии)
            angle = math.atan2(dy, dx)

            # Основная вершина (острие)
            tip_x = pos_x + math.cos(angle) * triangle_size
            tip_y = pos_y + math.sin(angle) * triangle_size

            # Боковые вершины
            left_x = pos_x + math.cos(angle + 2.5) * triangle_size * 1.2
            left_y = pos_y + math.sin(angle + 2.5) * triangle_size * 1.2

            right_x = pos_x + math.cos(angle - 2.5) * triangle_size * 1.2
            right_y = pos_y + math.sin(angle - 2.5) * triangle_size * 1.2

            # Рисуем треугольник
            points = [(tip_x, tip_y), (left_x, left_y), (right_x, right_y)]
            pygame.draw.polygon(surface, triangle_color, points)

            # Обводка треугольника
            pygame.draw.polygon(surface, (0, 0, 0), points, 3)

    # Рисуем точки на концах линии
    pygame.draw.circle(surface, (255, 255, 255), line_start, 2)
    pygame.draw.circle(surface, (255, 255, 255), line_end, 2)