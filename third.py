import pygame
import math

# инициализация Pygame
pygame.init()

# размеры окна
size = width, height = 800, 800

# создание окна
screen = pygame.display.set_mode((size))

# установка названия окна
pygame.display.set_caption("Шарики")


# радиус и скорость шарика
speed = 100

# список координат и скоростей шариков
balls = []

# обработчик событий
while True:
    for event in pygame.event.get():
        # если нажата левая кнопка мыши
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # получение координат курсора мыши
            pos = pygame.mouse.get_pos()
            # добавление координат и скоростей нового шарика
            balls.append([pos[0], pos[1], speed / math.sqrt(2), -speed / math.sqrt(2)])

    # закраска фона
    screen.fill((0, 0, 0))

    # отрисовка и движение шариков
    for ball in balls:
        # отрисовка шарика
        pygame.draw.circle(screen, (255, 255, 255), [int(ball[0]), int(ball[1])], 10)
        # обновление координат
        ball[0] += ball[2] / 60
        ball[1] += ball[3] / 60
        # проверка на столкновение со стенками окна
        if ball[0] < 10 or ball[0] > width - 10:
            ball[2] = -ball[2]
        if ball[1] < 10 or ball[1] > height - 10:
            ball[3] = -ball[3]

    # обновление окна
    pygame.display.update()

    # задержка
    pygame.time.delay(10)