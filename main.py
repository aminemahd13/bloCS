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

#Demander puis recevoir tout les changements de blocs et entitées
#Demander d'ajouter le joueur

#Create the player
running = entities.initialize(player_name = player_name) #Ecran d'accueil. Renvoie True si l'utilisateur veut jouer
# Game loop
clock = pygame.time.Clock()

while running:
    #Envoyer les données du clavier et de la souris
    #Recevoir les données et actualiser background et entities
    entities.render(player_name = player_name , background = background)

    
    # Update the screen
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

entities.close(player_name)