import pygame
import utils.key_handler as key
from resources import resources

def display_menu(screen):
    # Load background music
    pygame.mixer.init()
    pygame.mixer.music.load(resources("assets/audio/menu.mp3"))
    pygame.mixer.music.play(-1)  # Loop the music

    # Load background image
    background = pygame.image.load(resources("assets/graphics/loading.png"))
    background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))

    # Font settings
    font = pygame.font.Font(None, 72)
    button_font = pygame.font.Font(None, 48)

    # Menu options
    options = ["Start Game", "Tips", "Quit"]
    selected_option = 0

    while True:
        screen.blit(background, (0, 0))

        # Display menu options
        for i, option in enumerate(options):
            color = (255, 255, 255) if i == selected_option else (100, 100, 100)
            text = button_font.render(option, True, color)
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2 + i * 60))

        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                return "Quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    pygame.mixer.music.stop()
                    return options[selected_option]

def display_tips(screen):
    # Load background image
    background = pygame.image.load(resources("assets/graphics/loading.png"))
    background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))

    # Tips
    tips = [
        "Use the arrow keys to move.",
        "Use the mouse to place and remove blocks.",
        "Press 1-5 to select different blocks.",
        "Right-click to remove blocks.",
        "Left-click to place blocks.",
        "Press ESC to quit the game."
    ]

    # Font settings
    font = pygame.font.Font(None, 36)

    while True:
        screen.blit(background, (0, 0))

        # Display tips
        for i, tip in enumerate(tips):
            text = font.render(tip, True, (255, 255, 255))
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 100 + i * 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return