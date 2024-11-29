import pygame
import threading
from classes.class_background import Background
from classes.class_entities import Entities
import utils.key_handler as key
from classes.class_client import MultiClient

received_data = {}
data_sent = {}

client = MultiClient()

# Connect to the server
client.connect()

def send_data_continuously():
    while running:
        client.send_dict(data_sent)
        pygame.time.wait(100)  # Attendre 100ms avant d'envoyer à nouveau

def receive_data_continuously():
    global received_data
    while running:
        received_data = client.received_data()
        pygame.time.wait(100)  # Attendre 100ms avant de recevoir à nouveau

# Start threads for sending and receiving data
send_thread = threading.Thread(target=send_data_continuously)
receive_thread = threading.Thread(target=receive_data_continuously)
send_thread.start()
receive_thread.start()

#Faire un truc qui envoie en continu data_sent au serveur et qui réceptionne received_data


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
running = entities.initialize(player_name = player_name) #Ecran d'accueil. Renvoie True si l'utilisateur veut jouer

#Si l'utilisateur veut jouer, alors on envoie une requête au serveur
#Il faut y avoir le nom du joueur et ses dimensions d'écran
#Lorsque cette requête est acceptée, on recoit un truc qui nous indique qu'on peut jouer
#On doit recevoir notre identifiant de joueur
player_id = 0

# Game loop
clock = pygame.time.Clock()

while running:
    """
    received_data = {
        "Player" : {
            "player_id1" : {
                "name" : "Player 1",
                "loaded_game" : True,
                "map" : "Mine",
                "is_playing_2048" : False,
                "grille" : [[0,0,0,0],[0,0,0,0],[0,0,0,0]],
                "selected_block" : 1,
                "inventory" : {
                    "Dirt" : 10,
                    "Stone" : 0,
                    "Obsidian" : 0,
                    "Bedrock" : 0
                },
                "skin_name" : "Standing Right",
                "health" : 100,
                "x" : 30,
                "y" : 70,
                "running" : True
            }
        },
        
        "Mob" : {
            "mob_id1" : {
                "map" : "Mine",
                "type" : "Zombie",
                "skin_name" : "Standing Left",
                "health" : 100,
                "x" : 20,
                "y" : 0
            }
        }
    }
    """
    #On actualise la data reçue de la part du serveur
        
    data_sent = {
        "right" : key.right(),
        "left" : key.left(),
        "up" : key.up(),
        "echap" : key.close(),
        "number" : key.get_number(),
        "click" : None
    }
    #On regare où il click et on actualise data_sent en conséquence
    #S'il click, data_sent["click"] = [x_screen , y_screen , id_du_click (1 ou 3)]
    #Sinon, data_sent["click"] = None
    
    entities.recup_data(received_data)
    
    entities.render(player_name = player_name , background = background)

    
    # Update the screen
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

entities.close(player_name)

#On dit au serveur qu'on quitte le jeu