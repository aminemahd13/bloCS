import pygame
import asyncio
from classes.class_client import GameClient
import utils.key_handler as key
from screens.loading_screen import display_loading_screen
from screens.menu import display_menu, display_tips

async def main():
    pygame.init()

    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("bloCS - Menu")
    # Display the menu
    while True:
        choice = display_menu(screen)
        if choice == "Start Game":
            break
        elif choice == "Tips":
            display_tips(screen)
        elif choice == "Quit":
            pygame.quit()
            exit()

    # Display the loading screen
    display_loading_screen(screen)

    del screen


    player_name = "Player 1"
    height_screen = 1080
    width_screen = 1920


    client = GameClient(host = "127.0.0.1", port = 8888)
    server_task = asyncio.create_task(client.connect_to_server(player_name , height_screen , width_screen))


    if client.running:
        client_task = asyncio.create_task(client.handle_connection2())
        # Game loop
        clock = pygame.time.Clock()

        while client.running:
            client.render()
            # Update the screen
            pygame.display.flip()
            
            if key.close():
                client.running = False
            
            # Cap the frame rate
            clock.tick(30)

        await client.close()
    server_task.cancel()

if __name__ == "__main__":
    asyncio.run(main())