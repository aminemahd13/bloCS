import pygame
import sys
import logging
from classes.class_client import GameClient
from screens.menu import display_menu, display_tips
from screens.loading_screen import display_loading_screen

def setup_file_logging():
    file_handler = logging.FileHandler('client.log')
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_handler)
    
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)
    logging.getLogger().addHandler(stream_handler)

def main():
    setup_file_logging()
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("Multiplayer Game")

    # Menu loop
    while True:
        choice = display_menu(screen)
        if choice == "Start Game":
            break
        elif choice == "Tips":
            display_tips(screen)
        elif choice == "Quit":
            pygame.quit()
            sys.exit()

    # Display loading screen
    display_loading_screen(screen)
    
    # Game setup
    player_name = "Player 1"
    height_screen = 1080
    width_screen = 1920

    # Initialize client
    client = GameClient(host="127.0.0.1", port=55000)
    logging.info("Trying to connect to server...")
    client.connect_to_server(player_name, height_screen, width_screen)
    logging.info("Connection status: %s", client.running)
    
    # Game loop
    clock = pygame.time.Clock()
    try:
        while client.running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    client.running = False
                # Handle other events...
            
            logging.debug("Processing game loop events")
            # Game updates
            client.update()

            # Draw game elements here
            pygame.display.flip()

            # Cap framerate
            clock.tick(60)
    except Exception as e:
        logging.error(f"Error in main game loop: {e}")
    finally:
        # Cleanup
        client.disconnect()
        logging.info("Client disconnected")
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()