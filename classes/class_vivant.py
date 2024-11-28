from classes.class_block import DirtBlock, StoneBlock, WoodBlock, BedrockBlock, ObsidianBlock
from utils.textures import PlayerSkin, ZombieSkin

class Vivant:
    def __init__(self , type : str , x_spawn : int , y_spawn : int , health : int , dx : int):
        # [x,y] à changer en fonction du milieu de la map
        """Initializes the player
        name --> string, name of the player
        coordinates --> list of 2 integers [x,y] if coordinates = None then the player will be placed at the center of the map
        skin --> string, path to the skin of the player
        inventory --> list of items in the inventory
        health --> life points of the player
        """
        self.type = type
        self.taille_block = 40
        self.x = x_spawn * self.taille_block
        self.y = y_spawn * self.taille_block
        self.health = health
        self.dict_skins = eval(f"{type}Skin")
        self.skin = self.dict_skins["Standing Right"]
        self.skin_name = "Standing Right"
    
    def change_skin(self):
        self.skin = self.dict_skins[self.skin_name]
    
    def render(self , player):
        """
        Affiche le mob sur l'écran.
        """
        x_screen = self.x - player.x + player.x_screen
        y_screen = self.y - player.y + player.y_screen
        player.screen.blit(self.skin, (x_screen, y_screen))

    

"""
Utilisation

mob = Vivant(type : str , x_spawn : int , y_spawn : int , health : int , dx : int)
type : "Zombie","Player",...
x_spawn = indice bloc en haut de spawn
y_spawn = indice bloc en haut de spawn
health = vie
dx = déplacement sur les cotés


mob.render(screen , player)
Affiche le mob sur l'écran du joueur

mob.y_up(), mob.y_down(), mob.x_left(), mob.x_right()
Coordonnées des pixels au bord du mob

mob.take_damage(damage)
Attaque le mib. Renvoie True s'il est mort

mob.block_near
liste de blocs aux alentours du mob
"""