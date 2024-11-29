import pygame

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

def draw_quit_button(screen):
    button_color = (255, 69, 58)
    button_rect = pygame.Rect(50, 50, 200, 60)  # Rectangle du bouton
    pygame.draw.rect(screen, button_color, button_rect, border_radius=10)

    text = FONT.render("Quitter", True, (255, 255, 255))
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)


# Main game loop
def jeu(grid, screen):
    draw_grid(grid, screen)
    # Dessiner le bouton Quitter
    draw_quit_button(screen)




