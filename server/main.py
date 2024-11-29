import pygame
import threading
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

def update_received_data():
    global received_data
    while True:
        received_data = server.shared_data
        pygame.time.wait(100)  # Attendre 100ms avant de mettre à jour à nouveau

def send_data_entities():
    while True:
        data_entities = entities.recup_and_crea_data(received_data)
        pygame.time.wait(100)  # Attendre 100ms avant d'envoyer à nouveau

# Start server
server_thread = threading.Thread(target=server.start_server)
server_thread.start()

# Start threads for updating and sending data
update_thread = threading.Thread(target=update_received_data)
send_thread = threading.Thread(target=send_data_entities)
update_thread.start()
send_thread.start()

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