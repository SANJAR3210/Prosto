import pygame
import math

# Инициализация Pygame
pygame.init()

# Создание окна
size = width, height = 800, 800
screen = pygame.display.set_mode((size))
pygame.display.set_caption("Шарики")

# Класс для представления шарика
class Ball():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 100
        self.angle = math.radians(45)

    def update(self, dt):
        # Вычисление новых координат шарика
        dx = self.speed * math.cos(self.angle) * dt
        dy = -self.speed * math.sin(self.angle) * dt
        self.x -= dx
        self.y += dy

        # Проверка столкновения с границами окна
        if self.x - 10 < 0 or self.x + 10 > width:
            self.angle = math.pi - self.angle
        if self.y - 10 < 0 or self.y + 10 > height:
            self.angle = -self.angle

    def draw(self):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), 10)

# Список шариков
balls = []
running = True
clock = pygame.time.Clock()
while running:
    dt = clock.tick(60) / 1000  # Вычисление времени, прошедшего с предыдущего кадра
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            ball = Ball(event.pos[0], event.pos[1])
            balls.append(ball)
    screen.fill((0, 0, 0))
    # Обновление и рисование каждого шарика
    for ball in balls:
        ball.update(dt)
        ball.draw()
    pygame.display.flip()
pygame.quit()
