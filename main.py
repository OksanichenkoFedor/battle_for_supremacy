import pygame
import math
import threading
import queue
import time
import random
import sys

from attack_line import draw_line
from consts import WIDTH, HEIGHT, HEX_COLORS, HEX_COUNT, BACKGROUND_COLOR
from field import Field
from hexagon import Hexagon
from load_button import LoadButton
from painting import Painting

# Количество шестиугольников на стороне

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Битва за господство")

# Цвета
  # Серый

# Очередь для коммуникации между потоками
command_queue = queue.Queue()





def generate_hexagonal_grid(radius):
    """Генерирует шестиугольную сетку с заданным радиусом"""
    hexagons = []
    for q in range(-radius, radius + 1):
        for r in range(-radius, radius + 1):
            s = -q - r
            if abs(s) <= radius:
                hexagons.append(Hexagon(q, r, color=HEX_COLORS[(abs(q) + abs(r) + abs(-q - r)) % len(HEX_COLORS)]))
    return hexagons


def input_thread():
    """Поток для обработки пользовательского ввода"""
    print(f"=== Шестиугольное поле ===")
    print("Доступные команды:")
    print("- Введите число N: изменить цвет N случайных шестиугольников")
    print("- 'reset': вернуть все шестиугольники к исходным цветам")
    print("- 'quit': выйти из программы")
    print("=" * 30)

    while True:
        try:
            user_input = input("Введите команду: ").strip().lower()

            if user_input == "quit":
                command_queue.put(("quit", None))
                break
            elif user_input == "reset":
                command_queue.put(("reset", None))
                print("Команда 'reset' отправлена")
            else:
                try:
                    n = int(user_input)
                    if n < 0:
                        print("Пожалуйста, введите положительное число")
                        continue
                    command_queue.put(("change_color", n))
                    print(f"Команда на изменение {n} шестиугольников отправлена")
                except ValueError:
                    print("Пожалуйста, введите число или команду 'reset'/'quit'")

        except EOFError:
            command_queue.put(("quit", None))
            break
        except KeyboardInterrupt:
            command_queue.put(("quit", None))
            break


def main():
    clock = pygame.time.Clock()
    running = True

    # Генерируем поле
    field = Field(HEX_COUNT, screen)
    painting = Painting(screen)

    load_button = LoadButton(20, HEIGHT - 60, 120, 40, "Загрузить", field, screen)
    #field.load_button = load_button

    # Запускаем поток ввода в фоновом режиме
    input_thread_obj = threading.Thread(target=input_thread, daemon=True)
    input_thread_obj.start()

    field.draw()
    painting.draw()
    load_button.draw()
    drawing_line = False
    attack_color_id, defend_color_id = None, None
    while running:
        # Обработка событий Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:# Правая кнопка мыши
                    mouse_pos = pygame.mouse.get_pos()
                    id = field.contains_point(mouse_pos)
                    if id != -1:
                        if field.hexagons[id].color_id!=-1:
                            attack_color_id = field.hexagons[id].color_id
                            field.change_color(id, painting.get_current_color_id())

                            drawing_line = True
                            line_start = pygame.mouse.get_pos()
                            line_end = line_start
                elif event.button == 1:  # Левая кнопка мыши
                    mouse_pos = pygame.mouse.get_pos()
                    if load_button.is_clicked(mouse_pos):
                        field.draw()
                        painting.draw()
                        load_button.draw()
                        field.draw_status()
                    button_clicked = False
                    id = painting.is_clicked(mouse_pos)
                    if id!=-1:
                        button_clicked = True
                        painting.parce_clicking(id)
                        painting.draw()


                    if not button_clicked:
                        id = field.contains_point(mouse_pos)
                        if id != -1:
                            field.change_color(id, painting.get_current_color_id())
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3 and drawing_line:  # Отпускание правой кнопки
                    # Завершение рисования линии
                    id = field.contains_point(pygame.mouse.get_pos())
                    if id != -1:
                        defend_color_id = field.hexagons[id].color_id
                        field.attack(attack_color_id, defend_color_id)
                        field.update()
                        field.draw()
                        painting.draw()
                        load_button.draw()
                        field.draw_status()
                        line_end = pygame.mouse.get_pos()
                    else:
                        line_end = None
                    drawing_line = False
            elif event.type == pygame.MOUSEMOTION:
                if drawing_line:
                    # Обновляем конец линии при движении мыши
                    line_end = pygame.mouse.get_pos()



        # Обработка команд из очереди
        try:
            while True:
                command, data = command_queue.get_nowait()

                if command == "quit":
                    running = False
                elif command == "reset":
                    # Сбрасываем все шестиугольники к исходным цветам
                    field.reset()
                    field.draw()
                    #print("Все шестиугольники сброшены к исходным цветам")
                elif command == "change_color":
                    n = data
                    if n > field.total_hexagons:
                        n = field.total_hexagons

                    # Случайные цвета для изменения
                    colors = [(random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
                              for _ in range(n)]

                    # Выбираем случайные шестиугольники
                    indices = random.sample(range(field.total_hexagons), n)

                    # Изменяем цвет выбранных шестиугольников
                    for id, color in zip(indices, colors):
                        field.change_color(id, color)


                    print(f"Изменен цвет {n} шестиугольников")

        except queue.Empty:
            pass

        # Отрисовка
        field.draw()
        painting.draw()
        load_button.draw()
        field.draw_status()
        if drawing_line:
            draw_line(screen, line_start, line_end, attack_color_id)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()