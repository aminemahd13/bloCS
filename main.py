import pygame
from classes.class_background import Background
from classes.class_block import DirtBlock, StoneBlock, WoodBlock, BedrockBlock, ObsidianBlock
from classes.class_player import Player
import utils.key_handler as key
from utils.coord_to_screen import screen_to_coord
from screens.menu import display_menu, display_tips
from screens.loading_screen import display_loading_screen
from resources import resources
"""
the player inventory is updated when he breaks a block
the function damage_block has been changed to add the 'player' argument !!!!
the player can onlyyy add and destroy blocks around him (i.e 80px around him)

"""


# Pygame initialization
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Colors
WHITE = (255, 255, 255)

# Create the game screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Terraria-like Game Test")

# Initialize the background
background = Background()
#Create the player
player=Player(height_screen = SCREEN_HEIGHT , width_screen = SCREEN_WIDTH , name = "Player 1")
in_game =  False


# Game loop
running = True
clock = pygame.time.Clock()

# Initialize mixer for background music
pygame.mixer.init()

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

# Play game background music
pygame.mixer.music.load(resources("assets/audio/game.mp3"))
pygame.mixer.music.play(-1)  # Loop the music

while running:     
    
    running = player.do_events(background = background)
    
    in_game = player.play_2048(screen = screen , in_game = in_game)
        
    if not in_game and key.close() and not player.hist_touches["close"]: # Si on clique sur échap, le jeu se ferme
        running = False
    
    if not player.is_playing_2048:
        # Clear the screen
        screen.fill(WHITE)

        # Render the background and players
        background.render(screen = screen , player = player) # Affiche le background avec les blocs
        player.render(screen) # Affiche le joueur

        # Draw the inventory
        player.draw_inventory(screen)
        
        player.move()
        
        # Check if mod change is allowed
        player.change_map(background)
    

    # Update the screen
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.mixer.music.stop()
pygame.quit()
