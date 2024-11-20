from classes.class_block import Block, DirtBlock, StoneBlock, WoodBlock, BedrockBlock, ObsidianBlock , Wood1Block , Wood2Block , DoorupBlock , DoordownBlock, BackgroundBlock
from classes.class_player import Player
from utils.coord_to_screen import coord_to_screen, screen_to_coord, coord_to_indice
import pygame



        

def generation_rect_to_pts(liste : list) -> list:
    """
    Renvoie une liste de points en fct des rectangles.
    """
    liste_result = []
    for rect in liste:
        for x in range(rect[0] , rect[2] + 1):
            for y in range(rect[1] , rect[3] + 1):
                if [x,y] not in liste_result:
                    liste_result.append([x , y])
    return liste_result



class Background:
    def __init__(self , height : int , width : int, block_lists : dict):
        self.__height = height #Hauteur de l'écran
        self.__width = width #Largeur de l'écran
        self.__dict_block = {} #Dictionnaire contenant tout les blocs
        self.__taille_block = 40
        
        #On ajoute tout les blocs de type Dirt
        liste_dirt_coord = block_lists["Dirt"]
        liste_dirt_block = []
        for coord in liste_dirt_coord:
            liste_dirt_block.append(DirtBlock(x_indice = coord[0] , y_indice = coord[1]))
        self.__dict_block["Dirt"] = liste_dirt_block

        #On ajoute tout les blocs de type Stone
        liste_stone_coord = block_lists["Stone"]
        liste_stone_block = []
        for coord in liste_stone_coord:
            liste_stone_block.append(StoneBlock(x_indice = coord[0] , y_indice = coord[1]))
        self.__dict_block["Stone"] = liste_stone_block
        
        #Maison 
        
        liste_wood2_coord = block_lists["Wood2"]
        liste_wood2_block = []
        for coord in liste_wood2_coord:
                liste_wood2_block.append(Wood2Block(x_indice = coord[0] , y_indice = coord[1]))
        self.__dict_block["Wood2"] = liste_wood2_block
        
        #Inside
        liste_wood1_coord = generation_rect_to_pts([(36,3,41,7)])
        liste_wood1_coord.append([37,2]); liste_wood1_coord.append([38,2]); liste_wood1_coord.append([39,2]); liste_wood1_coord.append([40,2]); liste_wood1_coord.append([39,1]); liste_wood1_coord.append([38,1])
        liste_wood1_block = []
        for coord in liste_wood1_coord:
            if (coord != [39,7]) and (coord != [38,7]) and (coord != [39,6]) and (coord != [38,6]):
                liste_wood1_block.append(Wood1Block(x_indice = coord[0] , y_indice = coord[1]))
        self.__dict_block["Wood1"] = liste_wood1_block
        
        #Door
        liste_doorup_coord = [[39,6],[38,6]]
        liste_doorup_block = []
        for coord in liste_doorup_coord:
            liste_doorup_block.append(DoorupBlock(x_indice = coord[0] , y_indice = coord[1]))
        self.__dict_block["Doorup"] = liste_doorup_block
        
        liste_doordown_coord = [[39,7],[38,7]]
        liste_doordown_block = []
        for coord in liste_doordown_coord:
            liste_doordown_block.append(DoordownBlock(x_indice = coord[0] , y_indice = coord[1]))
        self.__dict_block["Doordown"] = liste_doordown_block
        
        
        #On ajoute tout les blocs de type Obsidian
        liste_obsidian_coord = block_lists["Obsidian"]
        liste_obsidian_block = []
        for coord in liste_obsidian_coord:
            liste_obsidian_block.append(ObsidianBlock(x_indice = coord[0] , y_indice = coord[1]))
        self.__dict_block["Obsidian"] = liste_obsidian_block
        
        #On ajoute tout les blocs de type Wood
        liste_wood_coord = block_lists["Wood"]
        liste_wood_block = []
        for coord in liste_wood_coord:
            liste_wood_block.append(WoodBlock(x_indice = coord[0] , y_indice = coord[1]))
        self.__dict_block["Wood"] = liste_wood_block
        
        #On ajoute tout les blocs de type Background
        liste_background_coord = block_lists["Background"]
        liste_background_block = []
        for coord in liste_background_coord:
            liste_background_block.append(BackgroundBlock(x_indice = coord[0] , y_indice = coord[1]))
        self.__dict_block["Background"] = liste_background_block

        #On ajoute tout les blocs de type Bedrock
        liste_bedrock_coord = block_lists["Bedrock"]
        liste_bedrock_block = []
        for coord in liste_bedrock_coord:
            liste_bedrock_block.append(BedrockBlock(x_indice = coord[0] , y_indice = coord[1]))
        self.__dict_block["Bedrock"] = liste_bedrock_block
     
    
    def check_block(self , x : int = None , y : int = None , x_indice : int = None , y_indice : int = None) -> Block:
        """
        Renvoie le bloc en x , y.
        """
        if x_indice is None:
            x_indice , y_indice = coord_to_indice(x = x , y = y)
        for liste in self.__dict_block.values():
            for block in liste:
                if block.x_indice == x_indice and block.y_indice == y_indice:
                    return block
            return None
    
    
    def add_block(self, block: Block) -> bool:
        """
        Ajoute un bloc dans le background.
        Renvoie True si le bloc a été placé, False sinon.
        """
        block_check = self.check_block(x_indice = block.x_indice ,  y_indice = block.y_indice)
        if block_check is None:
            self.__dict_block[block.type].append(block)
            return True
        return False

    def damage_block(self , damage : int, player : Player , x : int = None , y : int = None , x_indice : int = None , y_indice : int = None) -> bool:
        """
        Attaque le bloc se situant en x , y.
        S'il y avait un bloc qui a été détruit, renvoie True.
        Sinon, renvoie False.
        """
        if x_indice is None:
            x_indice , y_indice = coord_to_indice(x = x , y = y)
        for block_list in self.__dict_block.values():
            for block in block_list:
                if block.x_indice == x_indice and block.y_indice == y_indice:
                    if block.take_damage(damage):
                        block_list.remove(block)
                        player.inventory[block.type] += 1
                        return True
        return False
    
    
    def check_right(self , player : Player , deplacement : int) -> int:
        """
        Renvoie le déplacement maximal pouvant être effectué sur la droite,
        inférieur à déplacement.
        """
        for block in player.block_near:
            if block.is_solid:
                if block.y_down() >= player.y_up() and block.y_up() <= player.y_down(): #Si le bloc est sur la hauteur du joueur
                    if player.x_left() < block.x_left() <= player.x_right(): #Si le bloc est dans le joueur
                        deplacement = 0
                        break
                    elif block.x_left() > player.x_right(): #Si le bloc est sur la droite
                        deplacement = min(deplacement , block.x_left() - player.x_right() - 1)
        return deplacement
    
    
    def check_left(self , player : Player , deplacement : int) -> int:
        """
        Renvoie le déplacement maximal pouvant être effectué sur la gauche,
        inférieur à déplacement.
        """
        for block in player.block_near:
            if block.is_solid:
                if block.y_down() >= player.y_up() and block.y_up() <= player.y_down(): #Si le bloc est sur la hauteur du joueur
                    if player.x_left() <= block.x_right() < player.x_right(): #Si le bloc est dans le joueur
                        deplacement = 0
                        break
                    elif block.x_right() < player.x_left(): #Si le bloc est sur la gauche
                        deplacement = min(deplacement , player.x_left() - block.x_right() - 1)
        return deplacement
    
    
    def check_up(self , player : Player , deplacement : int) -> int:
        """
        Renvoie le déplacement maximal pouvant être effectué vers le haut,
        inférieur à déplacement.
        """
        for block in player.block_near:
            if block.is_solid:
                if block.x_left() <= player.x_right() and block.x_right() >= player.x_left(): #Si on est aligné verticalement au joueur
                    if player.y_up() <= block.y_down() < player.y_up() + self.__taille_block - 1:
                        deplacement = 0
                        break
                    elif block.y_down() < player.y_up():
                        deplacement = min(deplacement , player.y_up() - block.y_down() - 1)
        return deplacement
    
    
    def check_down(self , player : Player , deplacement : int) -> int:
        """
        Renvoie le déplacement maximal pouvant être effectué vers le bas,
        inférieur à déplacement.
        """
        for block in player.block_near:
            if block.is_solid:
                if block.x_left() <= player.x_right() and block.x_right() >= player.x_left(): #Si on est aligné verticalement au joueur
                    if player.y_up() +self.__taille_block < block.y_down() <= player.y_down():
                        deplacement = 0
                        break
                    elif block.y_up() > player.y_down():
                        deplacement = min(deplacement , block.y_up() - player.y_down() - 1)
        return deplacement
    
    
    def check_up_right(self , player : Player , deplacement_up : int , deplacement_right : int) -> tuple:
        deplacement_up1 = self.check_up(player = player , deplacement = deplacement_up)
        deplacement_right1 = self.check_right(player = player , deplacement = deplacement_right)
        if deplacement_up1 == deplacement_up and deplacement_right1 == deplacement_right:
            for block in player.block_near:
                if block.is_solid:
                    if block.x_left() <= player.x_right() + deplacement_right and block.x_right() >= player.x_left(): #Si on est aligné verticalement au joueur
                        if block.y_down() < player.y_up():
                            deplacement_up1 = min(deplacement_up1 , player.y_up() - block.y_down() - 1)
                    if block.y_down() >= player.y_up() - deplacement_up and block.y_up() <= player.y_down(): #Si le bloc est sur la hauteur du joueur
                        if block.x_left() > player.x_right(): #Si le bloc est sur la droite
                            deplacement_right1 = min(deplacement_right1 , block.x_left() - player.x_right() - 1)
            if deplacement_up1 == deplacement_up and deplacement_right1 == deplacement_right:
                return deplacement_up1 , deplacement_right1
            elif deplacement_up1 >= deplacement_right1:
                return deplacement_up1 , deplacement_right
            else:
                return deplacement_up , deplacement_right1
        else:
            return deplacement_up1 , deplacement_right1
        
                
    
    def check_up_left(self , player : Player , deplacement_up : int , deplacement_left : int) -> tuple:
        deplacement_up1 = self.check_up(player = player , deplacement = deplacement_up)
        deplacement_left1 = self.check_left(player = player , deplacement = deplacement_left)
        if deplacement_up1 == deplacement_up and deplacement_left1 == deplacement_left:
            for block in player.block_near:
                if block.is_solid:
                    if block.x_left() <= player.x_right() and block.x_right() >= player.x_left() - deplacement_left: #Si on est aligné verticalement au joueur
                        if block.y_down() < player.y_up():
                            deplacement_up1 = min(deplacement_up1 , player.y_up() - block.y_down() - 1)
                    if block.y_down() >= player.y_up() - deplacement_up and block.y_up() <= player.y_down(): #Si le bloc est sur la hauteur du joueur
                        if block.x_right() < player.x_left(): #Si le bloc est sur la droite
                            deplacement_left1 = min(deplacement_left1 , player.x_left() - block.x_right() - 1)
            if deplacement_up1 == deplacement_up and deplacement_left1 == deplacement_left:
                return deplacement_up1 , deplacement_left1
            elif deplacement_up1 >= deplacement_left1:
                return deplacement_up1 , deplacement_left
            else:
                return deplacement_up , deplacement_left1
        else:
            return deplacement_up1 , deplacement_left1
    
    
    def check_down_right(self , player : Player , deplacement_down : int , deplacement_right : int) -> tuple:
        deplacement_down1 = self.check_down(player = player , deplacement = deplacement_down)
        deplacement_right1 = self.check_right(player = player , deplacement = deplacement_right)
        if deplacement_down1 == deplacement_down and deplacement_right1 == deplacement_right:
            for block in player.block_near:
                if block.is_solid:
                    if block.x_left() <= player.x_right() + deplacement_right and block.x_right() >= player.x_left(): #Si on est aligné verticalement au joueur
                        if block.y_up() > player.y_down():
                            deplacement_down1 = min(deplacement_down1 , block.y_up() - player.y_down() - 1)
                    if block.y_down() >= player.y_up() and block.y_up() <= player.y_down() + deplacement_down: #Si le bloc est sur la hauteur du joueur
                        if block.x_left() > player.x_right(): #Si le bloc est sur la droite
                            deplacement_right1 = min(deplacement_right1 , block.x_left() - player.x_right() - 1)
            if deplacement_down1 == deplacement_down and deplacement_right1 == deplacement_right:
                return deplacement_down1 , deplacement_right1
            elif deplacement_down1 >= deplacement_right1:
                return deplacement_down1 , deplacement_right
            else:
                return deplacement_down , deplacement_right1
        else:
            return deplacement_down1 , deplacement_right1
    
    
    def check_down_left(self , player : Player , deplacement_down : int , deplacement_left : int) -> tuple:
        deplacement_down1 = self.check_down(player = player , deplacement = deplacement_down)
        deplacement_left1 = self.check_left(player = player , deplacement = deplacement_left)
        if deplacement_down1 == deplacement_down and deplacement_left1 == deplacement_left:
            for block in player.block_near:
                if block.is_solid:
                    if block.x_left() <= player.x_right() and block.x_right() >= player.x_left() - deplacement_left: #Si on est aligné verticalement au joueur
                        if block.y_up() > player.y_down():
                            deplacement_down1 = min(deplacement_down1 , block.y_up() - player.y_down() - 1)
                    if block.y_down() >= player.y_up() and block.y_up() <= player.y_down() + deplacement_down: #Si le bloc est sur la hauteur du joueur
                        if block.x_right() < player.x_left(): #Si le bloc est sur la droite
                            deplacement_left1 = min(deplacement_left1 , player.x_left() - block.x_right() - 1)
            if deplacement_down1 == deplacement_down and deplacement_left1 == deplacement_left:
                return deplacement_down1 , deplacement_left1
            elif deplacement_down1 >= deplacement_left1:
                return deplacement_down1 , deplacement_left
            else:
                return deplacement_down , deplacement_left1
        else:
            return deplacement_down1 , deplacement_left1
    
    
    def render(self, player : Player, screen) -> None:
        """
        Affiche le background.
        """
        player.block_near = []
        for liste in self.__dict_block.values():
            for block in liste:
                x_screen , y_screen = coord_to_screen(x = block.x , y = block.y , player = player)
                if 1 - self.__taille_block <= x_screen <= self.__width and 1 - self.__taille_block <= y_screen <= self.__height:
                    #On affiche uniquement les blocs qui se situent dans la map
                    block.render(screen = screen , player = player)
                    if player.x_left() - 50 <= block.x_right() and block.x_left() <= player.x_right() + 50 and player.y_up() - 50 <= block.y_down() and block.y_up()<= player.y_down() + 50:
                        player.block_near.append(block)
                    
    




"""

# Pygame initialization
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Create the game screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Terraria-like Game Test")

# Colors
WHITE = (255, 255, 255)

background = Background(width = 1920 , height = 1080)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(WHITE)

    # Render the background and blocks
    background.render(screen)

    # Example interaction (move blocks or damage a block)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        background.right(5)
    if keys[pygame.K_LEFT]:
        background.left(5)
    if keys[pygame.K_DOWN]:
        background.down(5)
    if keys[pygame.K_UP]:
        background.up(5)

    # Update the screen
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
"""

"""
Utilisation



Initialisation du background :
background = Background(width : int , height : int)



Déplacer le joueur à droite (<=> déplacer le background à gauche) de deplacement pixels :
background.right(deplacement : int) -> None



Déplacer le joueur à gauche (<=> déplacer le background à droite) de deplacement pixels :
background.left(deplacement : int) -> None



Déplacer le joueur en haut (<=> déplacer le background en bas) de deplacement pixels :
background.up(deplacement : int) -> None



Déplacer le joueur à bas (<=> déplacer le background en haut) de deplacement pixels :
background.down(deplacement : int) -> None



background.add_block(block : Block , decalage_auto : bool = True) -> bool
Ajoute un bloc en x,y.
Renvoie True si le bloc a été placé (s'il y avait pas de bloc ici), False sinon.

Remarque : Imaginons qu'un bloc peut être placé en coordonnées haut-gauche (0,0) pour avoir le bon décalage
avec le reste de la map. Si on veut ajouter le bloc en (1,1), ça va automatiquement le mettre
en (0,0) pour avoir le bon décalage avec le reste de la map.
Cette option peut être désactivée.



background.damage_block(x : int , y : int , damage : int) -> bool
Attaque le bloc, s'il existe, en x,y.
Renvoie True s'il y avait un bloc qui a été détruit, False sinon.



background.check_block(x : int , y : int) -> Block
Renvoie le bloc se situant en x,y.
Renvoie None s'il n'y a pas de block.



background.render() -> None
Affiche le background.



"""