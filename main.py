import pygame
from classes.class_background import Background
from classes.class_entities import Entities
from classes.class_server import MultiClientServer
from copy import deepcopy

server = MultiClientServer()

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
    
    received_data = deepcopy(MultiClientServer.shared_data)
    """
    received_data = {
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
        },
        "wanna_join" : [["player_name" , 1080 , 1920]],
        "wanna_quit" : [["player_id"]]
    } 
    """
    #Faire en sorte que ça soit la data envoyée des utilisateurs
    #On actualise le dict s'il y a de nouvelles valeurs d'entrée
    
    data_entities = entities.recup_and_crea_data(received_data)
    server.send_data(data_entities)
    
    #Faire un truc où dès qu'un joueur voulant venir a été accepté, on lui dit que c'est bon et on lui envoie son id de joueur

    clock.tick(30)