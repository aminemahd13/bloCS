import pygame
from class_background import Background
from class_block import DirtBlock, StoneBlock, WoodBlock, BedrockBlock

# Pygame initialization
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)

# Create the game screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Terraria-like Game Test")

# Initialize the background
background = Background(SCREEN_HEIGHT, SCREEN_WIDTH)

# Add some blocks to the background
background.add_block(DirtBlock(100, 200))
background.add_block(StoneBlock(200, 200))
background.add_block(WoodBlock(300, 200))
background.add_block(BedrockBlock(400, 200))

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(WHITE)

    # Render the background and blocks
    background.render(screen)

    # Example interaction (move blocks or damage a block)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        background.right(5)
    if keys[pygame.K_LEFT]:
        background.left(5)
    if keys[pygame.K_DOWN]:
        background.down(5)
    if keys[pygame.K_UP]:
        background.up(5)

    # Simulate damaging a block at (150, 200)
    if keys[pygame.K_SPACE]:
        if background.damage_block(150, 200, 10):
            print("Block destroyed at (150, 200)!")

    # Update the screen
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
