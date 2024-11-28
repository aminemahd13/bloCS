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

# Game loop
clock = pygame.time.Clock()

while True:
    entities.play(background = background)
    entities.move()
    #On actualise la direction des joueurs avec les données reçues
    #On regarde si un joueur veut se connecter
    #On indique si un mob/joueur a été supprimé ou ajouté
    #On envoie la data des joueurs et des mobs
    #On envoie quel block a été placé/détruit
    data = entities.crea_data()

    # Cap the frame rate
    clock.tick(30)