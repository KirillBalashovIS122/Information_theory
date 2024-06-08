import pygame
import sys

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Pygame App")

# Цвета
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Параметры квадрата
square_size = 50
square_x = WIDTH // 2
square_y = HEIGHT // 2
square_speed = 5

# Основной игровой цикл
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Получение нажатых клавиш
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        square_x -= square_speed
    if keys[pygame.K_RIGHT]:
        square_x += square_speed
    if keys[pygame.K_UP]:
        square_y -= square_speed
    if keys[pygame.K_DOWN]:
        square_y += square_speed

    # Отрисовка
    SCREEN.fill(WHITE)
    pygame.draw.rect(SCREEN, BLUE, (square_x, square_y, square_size, square_size))
    pygame.display.flip()

    # Ограничение кадров в секунду
    clock.tick(60)
