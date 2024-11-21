import pygame
import sys
import random
from utils import key_handler

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
GRID_SIZE = 4
TILE_SIZE = 500 // GRID_SIZE
FONT_SIZE = TILE_SIZE // 2
PADDING = 10
BACKGROUND_COLOR = (187, 173, 160)
TILE_COLORS = {
    0: (204, 192, 179),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}
TEXT_COLOR = (119, 110, 101)

# Fonts
FONT = pygame.font.Font(None, FONT_SIZE)


# Helper Functions
def draw_grid(grid, screen , animation_offsets=None):
    screen.fill(BACKGROUND_COLOR)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            value = grid[row][col]
            rect_x = (col-2) * TILE_SIZE + SCREEN_WIDTH // 2
            rect_y = (row-2) * TILE_SIZE + SCREEN_HEIGHT // 2
            tile_color = TILE_COLORS.get(value, (60, 58, 50))

            # Apply animation offsets
            if animation_offsets and (row, col) in animation_offsets:
                offset_x, offset_y = animation_offsets[(row, col)]
                rect_x += offset_x
                rect_y += offset_y

            pygame.draw.rect(
                screen,
                tile_color,
                (rect_x, rect_y, TILE_SIZE - 2 * PADDING, TILE_SIZE - 2 * PADDING),
                border_radius=8,
            )

            if value != 0:
                text = FONT.render(str(value), True, TEXT_COLOR)
                text_rect = text.get_rect(center=(rect_x + TILE_SIZE // 2 - PADDING, rect_y + TILE_SIZE // 2 - PADDING))
                screen.blit(text, text_rect)


def spawn_new_tile(grid , value):
    empty_tiles = [(row, col) for row in range(GRID_SIZE) for col in range(GRID_SIZE) if grid[row][col] == 0]
    if empty_tiles:
        row, col = random.choice(empty_tiles)
        grid[row][col] = int(value)
        return True
    return False


def move(grid, direction):
    moved = False
    animation_offsets = {}
    original_grid = [row[:] for row in grid]

    def compress(row):
        new_row = [num for num in row if num != 0]
        new_row += [0] * (GRID_SIZE - len(new_row))
        return new_row

    def merge(row):
        for i in range(len(row) - 1):
            if row[i] != 0 and row[i] == row[i + 1]:
                row[i] *= 2
                row[i + 1] = 0
        return row

    for row in range(GRID_SIZE):
        if direction in ("LEFT", "RIGHT"):
            current_row = grid[row][:]
            if direction == "LEFT":
                current_row = compress(current_row)
                current_row = merge(current_row)
                current_row = compress(current_row)
            elif direction == "RIGHT":
                current_row = compress(current_row[::-1])
                current_row = merge(current_row)
                current_row = compress(current_row)[::-1]
            grid[row] = current_row

        elif direction in ("UP", "DOWN"):
            current_col = [grid[i][row] for i in range(GRID_SIZE)]
            if direction == "UP":
                current_col = compress(current_col)
                current_col = merge(current_col)
                current_col = compress(current_col)
            elif direction == "DOWN":
                current_col = compress(current_col[::-1])
                current_col = merge(current_col)
                current_col = compress(current_col)[::-1]
            for i in range(GRID_SIZE):
                grid[i][row] = current_col[i]

    moved = original_grid != grid
    return moved, animation_offsets


def is_game_over(grid):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == 0:
                return False
            if col < GRID_SIZE - 1 and grid[row][col] == grid[row][col + 1]:
                return False
            if row < GRID_SIZE - 1 and grid[row][col] == grid[row + 1][col]:
                return False
    return True


# Main game loop
def jeu(grid , screen):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if key_handler.closegame():
        return False
    elif key_handler.up():
        direction = "UP"
    elif key_handler.down():
        direction = "DOWN"
    elif key_handler.left():
        direction = "LEFT"
    elif key_handler.right():
        direction = "RIGHT"
    else:
        direction = None

    if direction:
        moved, _ = move(grid, direction)
        if moved:
            if is_game_over(grid):
                return False

    draw_grid(grid , screen)
    return True


