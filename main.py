import pygame
from classes.class_background import Background
from classes.class_entities import Entities
import utils.key_handler as key
from classes.class_client import MultiClient

client = MultiClient()


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
#Lorsque cette requête est acceptée, on recoit un truc qui nous indique qu'on peut jouer
#On doit recevoir notre identifiant de joueur
player_id = 0

# Game loop
clock = pygame.time.Clock()

while running:
    received_data = client.received_data()
    """
    received_data = {
        "Player" : {
            "player_id1" : {
                "name" : "Player 1",
                "loaded_game" : True,
                "map" : "Mine",
                "is_playing_2048" : False,
                "grille" : [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],
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
    
    entities.recup_data(received_data)
    
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
    
    client.send_dict(data_sent)
    
    entities.render(player_name = player_name , background = background)

    
    # Update the screen
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

entities.close(player_name)

#On dit au serveur qu'on quitte le jeu