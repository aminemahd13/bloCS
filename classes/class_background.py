from classes.class_block import Block, DirtBlock, StoneBlock, WoodBlock, BedrockBlock, ObsidianBlock , Wood1Block , Wood2Block , DoorupBlock , DoordownBlock, TuileBlock , GameBlock
from classes.class_player import Player
from utils.coord_to_screen import coord_to_screen, screen_to_coord, coord_to_indice, indice_to_screen, indices_randoms
import pygame
from utils.lists_blocks import block_lists
from utils.house_list import house_blocks



        

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
    def __init__(self , height : int , width : int):
        self.__height = height #Hauteur de l'écran
        self.__width = width #Largeur de l'écran
        self.mode = 1
        self.dict_block = {} #Dictionnaire contenant tout les blocs
        self.dict_block_background = {}
        self.dict_block_house = {}
        self.__taille_block = 40
        self.back_texture_path = "crea_map/map/background.png"
        self.back_texture = pygame.image.load(self.back_texture_path)
        self.back_texture = pygame.transform.scale(self.back_texture, (9360 , 3240))
        self.mod_change_allowed = True
        
        #On ajoute tout les blocs de type Game
        liste_game_coord = house_blocks["Game"]
        liste_game_block = []
        for coord in liste_game_coord:
            liste_game_block.append(GameBlock(x_indice = coord[0] , y_indice = coord[1]))
        self.dict_block_house["Game"] = liste_game_block
        
        #On ajoute tout les blocs de type Stone
        self.dict_block_house["Stone"] = []
        self.dict_block_house["Dirt"] = []
        self.dict_block_house["Obsidian"] = []
        self.dict_block_house["Bedrock"] = []
        self.dict_block_house["Wood"] = []
        
        #Maison 
        
        liste_wood2_coord = house_blocks["Wood2"]
        liste_wood2_block = []
        for coord in liste_wood2_coord:
                liste_wood2_block.append(Wood2Block(x_indice = coord[0] , y_indice = coord[1] , is_solid = True))
        self.dict_block_house["Wood2"] = liste_wood2_block
        
        #Inside
        liste_wood1_coord = house_blocks["Wood1"]
        liste_wood1_block = []
        for coord in liste_wood1_coord:
            if (coord != [39,7]) and (coord != [38,7]) and (coord != [39,6]) and (coord != [38,6]):
                liste_wood1_block.append(Wood1Block(x_indice = coord[0] , y_indice = coord[1]))
        self.dict_block_house["Wood1"] = liste_wood1_block
        
        #Door
        liste_doorup_coord = house_blocks["Doorup"]
        liste_doorup_block = []
        for coord in liste_doorup_coord:
            liste_doorup_block.append(DoorupBlock(x_indice = coord[0] , y_indice = coord[1]))
        self.dict_block_house["Doorup"] = liste_doorup_block
        
        liste_doordown_coord = house_blocks["Doordown"]
        liste_doordown_block = []
        for coord in liste_doordown_coord:
            liste_doordown_block.append(DoordownBlock(x_indice = coord[0] , y_indice = coord[1]))
        self.dict_block_house["Doordown"] = liste_doordown_block
        
        
        liste_tuile_block = []
        
        liste_air_coord = block_lists["Air"]
        indices_r = indices_randoms(liste_air_coord , 18)
        indices_r_2 = indices_r[0 : 12]
        indices_r_4 = indices_r[12 : 18]
        for i , coord in enumerate(liste_air_coord):
            if i in indices_r_2:
                liste_tuile_block.append(TuileBlock(x_indice = coord[0] , y_indice = coord[1] , value = 2))
            elif i in indices_r_4:
                liste_tuile_block.append(TuileBlock(x_indice = coord[0] , y_indice = coord[1] , value = 4))
        
        
        #On ajoute tout les blocs de type Dirt
        liste_dirt_coord = block_lists["Dirt"]
        indices_r = indices_randoms(liste_dirt_coord , 18)
        indices_r_8 = indices_r[0 : 12]
        indices_r_16 = indices_r[12 : 18]
        liste_dirt_block = []
        for i , coord in enumerate(liste_dirt_coord):
            if i in indices_r_8:
                liste_tuile_block.append(TuileBlock(x_indice = coord[0] , y_indice = coord[1] , value = 8))
            elif i in indices_r_16:
                liste_tuile_block.append(TuileBlock(x_indice = coord[0] , y_indice = coord[1] , value = 16))
            else:
                liste_dirt_block.append(DirtBlock(x_indice = coord[0] , y_indice = coord[1]))
        self.dict_block_background["Dirt"] = liste_dirt_block


        #On ajoute tout les blocs de type Stone
        liste_stone_coord = block_lists["Stone"]
        indices_r = indices_randoms(liste_stone_coord , 18)
        indices_r_32 = indices_r[0 : 12]
        indices_r_64 = indices_r[12 : 18]
        liste_stone_block = []
        for i , coord in enumerate(liste_stone_coord):
            if i in indices_r_32:
                liste_tuile_block.append(TuileBlock(x_indice = coord[0] , y_indice = coord[1] , value = 32))
            elif i in indices_r_64:
                liste_tuile_block.append(TuileBlock(x_indice = coord[0] , y_indice = coord[1] , value = 64))
            else:
                liste_stone_block.append(StoneBlock(x_indice = coord[0] , y_indice = coord[1]))
        self.dict_block_background["Stone"] = liste_stone_block
        
        #Maison 
        
        liste_wood2_coord = block_lists["Wood2"]
        liste_wood2_block = []
        for coord in liste_wood2_coord:
                liste_wood2_block.append(Wood2Block(x_indice = coord[0] , y_indice = coord[1]))
        self.dict_block_background["Wood2"] = liste_wood2_block
        
        #Inside
        liste_wood1_coord = block_lists["Wood1"]
        liste_wood1_block = []
        for coord in liste_wood1_coord:
            if (coord != [39,7]) and (coord != [38,7]) and (coord != [39,6]) and (coord != [38,6]):
                liste_wood1_block.append(Wood1Block(x_indice = coord[0] , y_indice = coord[1]))
        self.dict_block_background["Wood1"] = liste_wood1_block
        
        #Door
        liste_doorup_coord = block_lists["Doorup"]
        liste_doorup_block = []
        for coord in liste_doorup_coord:
            liste_doorup_block.append(DoorupBlock(x_indice = coord[0] , y_indice = coord[1]))
        self.dict_block_background["Doorup"] = liste_doorup_block
        
        liste_doordown_coord = block_lists["Doordown"]
        liste_doordown_block = []
        for coord in liste_doordown_coord:
            liste_doordown_block.append(DoordownBlock(x_indice = coord[0] , y_indice = coord[1]))
        self.dict_block_background["Doordown"] = liste_doordown_block
        
        
        #On ajoute tout les blocs de type Obsidian
        liste_obsidian_coord = block_lists["Obsidian"]
        indices_r = indices_randoms(liste_obsidian_coord , 25)
        indices_r_128 = indices_r[0 : 12]
        indices_r_256 = indices_r[12 : 24]
        indices_r_512 = indices_r[24]
        liste_obsidian_block = []
        for i , coord in enumerate(liste_obsidian_coord):
            if i in indices_r_128:
                liste_tuile_block.append(TuileBlock(x_indice = coord[0] , y_indice = coord[1] , value = 128))
            elif i in indices_r_256:
                liste_tuile_block.append(TuileBlock(x_indice = coord[0] , y_indice = coord[1] , value = 256))
            elif i in indices_r_512:
                liste_tuile_block.append(TuileBlock(x_indice = coord[0] , y_indice = coord[1] , value = 512))
            else:
                liste_obsidian_block.append(ObsidianBlock(x_indice = coord[0] , y_indice = coord[1]))
        self.dict_block_background["Obsidian"] = liste_obsidian_block
        
        #On ajoute tout les blocs de type Wood
        liste_wood_coord = block_lists["Wood"]
        liste_wood_block = []
        for coord in liste_wood_coord:
            liste_wood_block.append(WoodBlock(x_indice = coord[0] , y_indice = coord[1]))
        self.dict_block_background["Wood"] = liste_wood_block
        

        #On ajoute tout les blocs de type Bedrock
        liste_bedrock_coord = block_lists["Bedrock"]
        liste_bedrock_block = []
        for coord in liste_bedrock_coord:
            liste_bedrock_block.append(BedrockBlock(x_indice = coord[0] , y_indice = coord[1]))
        self.dict_block_background["Bedrock"] = liste_bedrock_block
        
        self.dict_block_background["Tuile"] = liste_tuile_block
        
        self.dict_block = self.dict_block_background
     
     
    
    def change_mod(self):
        if self.mode == 1:
            self.mode = 2
            self.dict_block_background = self.dict_block
            self.dict_block = self.dict_block_house
        else:
            self.mode = 1
            self.dict_block_house = self.dict_block
            self.dict_block = self.dict_block_background
        
    
    
    def check_block(self , x : int = None , y : int = None , x_indice : int = None , y_indice : int = None) -> Block:
        """
        Renvoie le bloc en x , y.
        """
        if x_indice is None:
            x_indice , y_indice = coord_to_indice(x = x , y = y)
        for liste in self.dict_block.values():
            for block in liste:
                if block.x_indice == x_indice and block.y_indice == y_indice:
                    return block
            return None
    
    
    def add_block(self, block: Block) -> bool:
        """
        Ajoute un bloc dans le background.
        Renvoie True si le bloc a été placé, False sinon.
        """
        for liste in self.dict_block.values():
            for block_check in liste:
                if block_check.x_indice == block.x_indice and block_check.y_indice == block.y_indice:
                    return False
        self.dict_block[block.type].append(block)
        return True

    def damage_block(self , damage : int, player : Player , x : int = None , y : int = None , x_indice : int = None , y_indice : int = None) -> bool:
        """
        Attaque le bloc se situant en x , y.
        S'il y avait un bloc qui a été détruit, renvoie True.
        Sinon, renvoie False.
        """
        if x_indice is None:
            x_indice , y_indice = coord_to_indice(x = x , y = y)
        for block_list in self.dict_block.values():
            for block in block_list:
                if block.x_indice == x_indice and block.y_indice == y_indice:
                    if block.take_damage(damage , player.tuile_max()):
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
        if self.mode == 1:
            x_screen , y_screen = indice_to_screen(x_indice = -2 * 39 , y_indice = 0 , player = player)
            screen.blit(self.back_texture, (x_screen , y_screen))
        player.block_near = []
        for liste in self.dict_block.values():
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