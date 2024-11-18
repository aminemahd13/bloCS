import pygame

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Render Block with Texture")

# Load the texture (ensure the path is correct)
texture = pygame.image.load("assets/graphics/dirt.jpeg")  # Replace with your file path
texture = pygame.transform.scale(texture, (50, 50))  # Optionally resize the texture

# Define the block's position (top-left corner)
block_position = (100, 100)  # x, y coordinates

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((0, 0, 0))  # Fill with black

    # Draw the block
    screen.blit(texture, block_position)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
