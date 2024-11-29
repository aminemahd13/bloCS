import pygame
from classes.class_background import Background
from classes.class_entities import Entities
from classes.class_server import MultiClientServer

received_data = {
    "Players" : {}
} #Donnée reçue des joueurs
data_entities = {}

server = MultiClientServer()

#Faire une sorte de thread qui actualise received_data en continu
#Et un autre qui envoie data_entities en continu
#Faire en sorte de pouvoir ajouter un joueur ou l'enlever en fonction des requêtes

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
    
    """
    received_data = {
        "Players" : {
            "player_id" : {
                "right" : False,
                "left" : False,
                "up" : False,
                "echap" : False,
                "number" : -1,
                "click" : None #ou [x_screen , y_screen , id_click (1 ou 3)]
            },
            "player2_id" : {
                "right" : False,
                "left" : False,
                "up" : False,
                "echap" : False,
                "number" : -1,
                "click" : None
            }
        }
    } 
    """
    
    data_entities = entities.recup_and_crea_data(received_data)
    
    #Faire un truc où dès qu'un joueur voulant venir a été accepté, on lui dit que c'est bon et on lui envoie son id de joueur

    clock.tick(30)