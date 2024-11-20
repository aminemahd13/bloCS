
import pygame
import time

def display_loading_screen(screen):
    # Load background image
    background = pygame.image.load("assets/graphics/loading.png")
    background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))

    # Loading tips
    tips = [
        "Tip 1: Use the arrow keys to move.",
        "Tip 2: Use the mouse to place and remove blocks.",
        "Tip 3: Press 1-5 to select different blocks.",
        "Tip 4: Right-click to remove blocks.",
        "Tip 5: Left-click to place blocks."
    ]

    # Font settings
    font = pygame.font.Font(None, 36)
    tip_font = pygame.font.Font(None, 28)

    # Display background
    screen.blit(background, (0, 0))

    # Display loading text
    loading_text = font.render("Loading...", True, (255, 255, 255))
    screen.blit(loading_text, (screen.get_width() // 2 - loading_text.get_width() // 2, screen.get_height() // 2 - 50))

    # Display a random tip
    tip_text = tip_font.render(tips[int(time.time()) % len(tips)], True, (255, 255, 255))
    screen.blit(tip_text, (screen.get_width() // 2 - tip_text.get_width() // 2, screen.get_height() // 2 + 10))

    # Update the display
    pygame.display.flip()

    # Simulate loading time
    time.sleep(3)