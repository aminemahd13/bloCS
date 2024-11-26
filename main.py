import pygame
from classes.class_background import Background
from classes.class_block import DirtBlock, StoneBlock, WoodBlock, BedrockBlock, ObsidianBlock
from classes.class_entities import Entities
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

player_name = "Player 1"
height_screen = 1080
width_screen = 1920

# Pygame initialization
pygame.init()

# Colors
WHITE = (255, 255, 255)

# Initialize entities
entities = Entities()
# Initialize the background
background = Background()

#Create the player
player_name = entities.add_player(player_name , height_screen , width_screen)
if entities.initialize(player_name): #Ecran d'accueil
    running = True
else:
    running = False

entities.add_mob("Zombie" , "Mine")

# Game loop
clock = pygame.time.Clock()

while running:
    entities.play(background , player_name)
    entities.move()
    entities.render(player_name , background)

    # Update the screen
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

# Quit Pygame
pygame.mixer.music.stop()
pygame.quit()


