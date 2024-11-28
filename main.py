import pygame
from classes.class_background import Background
from classes.class_entities import Entities

player_name = "Player 1"
height_screen = 1080
width_screen = 1920

# Pygame initialization
pygame.init()

# Initialize entities
entities = Entities()
# Initialize the background
background = Background()

#Create the player
player_name = entities.add_player(name = player_name , height_screen = height_screen , width_screen = width_screen)
running = entities.initialize(player_name = player_name) #Ecran d'accueil. Renvoie True si l'utilisateur veut jouer

entities.add_mob(type = "Zombie" , map = "Mine" , x_spawn = 10 , y_spawn = 0)

# Game loop
clock = pygame.time.Clock()

while running:
    running = entities.play(background = background , player_name = player_name)
    entities.move()
    entities.render(player_name = player_name , background = background)

    
    # Update the screen
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

entities.close(player_name)