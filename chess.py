import pygame
import sys

# Инициализация Pygame
pygame.init()

# Константы
BOARD_SIZE = 8
SQUARE_SIZE = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Создание окна
window_size = BOARD_SIZE * SQUARE_SIZE
screen = pygame.display.set_mode((window_size, window_size))
pygame.display.set_caption("Шахматы")

# Шрифты
font = pygame.font.SysFont(None, 48)

# Фигуры
pieces = {}

def create_pieces():
    for col in range(BOARD_SIZE):
        pieces[(1, col)] = ('P', WHITE)  # Белые пешки
        pieces[(6, col)] = ('P', BLACK)  # Черные пешки
    pieces[(0, 0)] = pieces[(0, 7)] = ('R', WHITE)  # Белые ладьи
    pieces[(7, 0)] = pieces[(7, 7)] = ('R', BLACK)  # Черные ладьи

def draw_board():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces():
    for (row, col), (piece, color) in pieces.items():
        piece_text = font.render(piece, True, RED)
        screen.blit(piece_text, (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4))

def main():
    create_pieces()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_board()
        draw_pieces()
        pygame.display.flip()

if __name__ == "__main__":
    main()
