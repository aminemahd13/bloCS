from classes.class_block import Block, DirtBlock, StoneBlock, WoodBlock, BedrockBlock, ObsidianBlock
from classes.class_player import Player
from utils.coord_to_screen import coord_to_screen, screen_to_coord, coord_to_indice
import pygame



 ############# added draw_inventory function #############


def draw_inventory(screen, player, selected_block):
    font = pygame.font.Font(None, int(36 * screen.get_height() / 1080))
    block_types = ["Dirt", "Stone", "Obsidian", "Wood", "Bedrock"]
    block_images = {
        "Dirt": pygame.image.load("assets/graphics/dirt.png"),
        "Stone": pygame.image.load("assets/graphics/stone.png"),
        "Obsidian": pygame.image.load("assets/graphics/obsidian.png"),
        "Wood": pygame.image.load("assets/graphics/dirt.png"),
        "Bedrock": pygame.image.load("assets/graphics/bedrock.png")
    }
    x_offset = 10
    y_offset = 10
    for i, block_type in enumerate(block_types):
        block_image = pygame.transform.scale(block_images[block_type], (int(40 * screen.get_height() / 1080), int(40 * screen.get_height() / 1080)))
        if i+1 == selected_block:
            pygame.draw.rect(screen, (0, 255, 0), (x_offset + i * int(90 * screen.get_height() / 1080) - 5, y_offset - 5, int(50 * screen.get_height() / 1080), int(50 * screen.get_height() / 1080)), 3)
        screen.blit(block_image, (x_offset + i * int(90 * screen.get_height() / 1080), y_offset))
        n = player.inventory[block_type]
        text = font.render(str(n), True, (0, 0, 0))
        screen.blit(text, (x_offset + i * int(90 * screen.get_height() / 1080) + int(45 * screen.get_height() / 1080), y_offset + int(10 * screen.get_height() / 1080)))



        

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
        self.__dict_block = {} #Dictionnaire contenant tout les blocs
        self.__taille_block = 40
        
        #On ajoute tout les blocs de type Dirt
        liste_dirt_coord = generation_rect_to_pts([(45,15,48,15),(46,16,47,16),(14,11,22,11), (18,7,18,7), (27,13,27,13), (32,13,32,13), (40,18,40,18), (40,15,41,17), (42,15,42,16), (43,15,43,15), (42,13,43,14), (44,12,49,14), (49,11,50,11), (50,12,53,13), (53,14,53,14), (56,11,56,11)])
        liste_dirt_block = []
        for coord in liste_dirt_coord:
            liste_dirt_block.append(DirtBlock(x_indice = coord[0] , y_indice = coord[1]))
        self.__dict_block["Dirt"] = liste_dirt_block

        #On ajoute tout les blocs de type Stone
        liste_stone_coord = generation_rect_to_pts([(45,25,45,25),(71,15,71,15),(63,22,64,22),(45,20,45,20), (46,24,47,25), (48,25,49,25), (49,22,52,22), (50,23,54,23), (51,24,59,24), (55,25,60,25), (58,22,58,22), (59,18,63,18), (63,21,66,21), (65,22,70,22), (68,23,72,24), (73,24,73,24), (65,16,67,16), (71,16,71,16), (72,15,73,16), (73,18,74,18), (73,20,73,21)])
        liste_stone_block = []
        for coord in liste_stone_coord:
            liste_stone_block.append(StoneBlock(x_indice = coord[0] , y_indice = coord[1]))
        self.__dict_block["Stone"] = liste_stone_block
        
        #On ajoute tout les blocs de type Obsidian
        liste_obsidian_coord = generation_rect_to_pts([(23,21,28,21),(10,17,10,17), (11,18,11,18), (11,16,12,17), (13,16,13,16), (12,15,21,15), (13,14,19,14), (19,16,26,16), (21,17,26,17), (11,20,11,20), (10,21,13,21), (9,22,15,22), (13,23,23,23), (16,24,22,24), (22,22,27,22), (23,22,28,22), (27,20,28,20), (28,19,28,19), (6,29,11,31), (6,32,18,35), (6,36,9,38), (7,38,10,37), (12,36,23,36), (13,37,16,38), (12,41,17,42), (12,43,21,43), (20,41,27,41), (11,45,14,45), (6,46,17,46), (3,47,15,47), (11,48,13,48), (11,49,22,49), (36,31,37,31), (35,32,45,32), (34,33,48,34), (35,35,48,36) ])
        liste_obsidian_block = []
        for coord in liste_obsidian_coord:
            liste_obsidian_block.append(ObsidianBlock(x_indice = coord[0] , y_indice = coord[1]))
        self.__dict_block["Obsidian"] = liste_obsidian_block
        
        #On ajoute tout les blocs de type Wood
        liste_wood_coord = generation_rect_to_pts([])
        liste_wood_block = []
        for coord in liste_wood_coord:
            liste_wood_block.append(WoodBlock(x_indice = coord[0] , y_indice = coord[1]))
        self.__dict_block["Wood"] = liste_wood_block

        #On ajoute tout les blocs de type Bedrock
        liste_bedrock_coord = generation_rect_to_pts([(27,19,27,19),(0,3,1,3), (4,3,14,3), (8,2,12,2), (0,4,13,8), (14,4,14,7),(14,4,14,7), (15,4,15,6), (16,5,16,5), (0,9,8,9), (0,10,5,10), (0,11,2,11), (16,9,16,9), (0,14,3,14), (0,15,4,26), (5,16,5,20), (6,18,6,20), (7,20,7,20), (5,25,45,26), (5,23,12,24), (13,24,15,24), (23,24,36,24), (24,23,35,23), (28,22,34,22), (29,21,33,21), (29,20,31,20), (29,19,30,19), (10,20,10,20), (11,19,11,19), (12,18,26,20), (14,16,18,16), (13,17,20,17), (14,21,22,21), (16,22,21,22), (9,17,9,17), (9,16,10,16), (8,15,11,15), (7,14,12,14), (6,13,26,13), (8,12,23,12), (20,14,27,14), (22,15,28,15), (27,16,28,16), (27,17,29,17), (27,18,29,18), (27,27,27,29), (20,2,25,2), (19,3,25,3), (19,4,26,4), (20,5,27,5), (19,6,30,6), (19,7,31,7), (18,8,20,8), (46,7,47,7), (51,7,67,7), (55,6,59,6), (55,5,57,5), (64,6,66,6), (31,8,68,8), (36,9,69,9), (33,10,69,10), (36,11,48,11), (51,11,55,11), (60,11,69,11), (63,12,64,12), (38,12,41,14), (42,12,43,12), (30,13,31,13), (33,13,34,13), (30,14,35,14), (31,15,39,15), (34,16,39,16), (35,17,39,17), (38,18,39,18), (39,19,47,19), (42,20,44,20), (46,20,46,20), (41,18,49,18), (42,17,53,17), (43,16,45,16), (44,15,44,15), (48,16,54,16), (49,15,55,15), (50,14,52,14), (40,24,44,24), (46,23,49,23), (48,24,50,24), (50,25,54,25), (46,26,76,26), (52,20,53,20), (51,21,56,21), (53,22,57,22), (59,22,61,22), (55,23,67,23), (63,22,64,22), (60,24,67,24), (61,25,76,25), (74,24,76,24), (73,23,76,23), (71,22,76,22), (67,21,72,21), (74,21,76,21), (63,20,72,20), (75,20,76,20), (58,19,70,19), (76,19,76,19), (64,18,65,18), (68,18,69,18), (75,18,76,18), (72,17,77,17), (74,16,76,16), (65,15,71,15), (74,15,76,15), (66,14,76,14), (68,13,75,13), (71,12,75,12), (72,11,74,11), (73,10,73,10), (57,16,61,16), (57,15,60,15), (58,14,59,14), (0,27,76,28), (0,29,5,46), (12,29,36,30), (12,31,35,31), (19,32,33,35), (34,32,34,32), (34,35,34,35), (24,36,34,36), (17,37,76,40), (6,38,6,38), (6,39,16,40), (0,41,11,44), (0,45,10,45), (0,46,5,46), (0,47,2,47), (0,48,10,53), (11,50,24,50), (11,51,76,53), (1,31,76,31), (9,32,76,32), (12,33,76,36), (18,41,19,41), (18,42,76,42), (22,43,76,43), (12,44,76,44), (15,45,76,45), (18,46,76,46), (16,47,76,47), (14,48,76,48), (23,49,76,49), (11,50,76,53)] )
        liste_bedrock_block = []
        enlever_bedrock=[[27,27],[27,28],[27,29],[45,25],[71,15],[63,22],[64,22],[77,17]]
        for coord in liste_bedrock_coord:
            if coord not in enlever_bedrock:
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
            if block.x_left() <= player.x_right() and block.x_right() >= player.x_left(): #Si on est aligné verticalement au joueur
                if player.y_up() +self.__taille_block < block.y_down() <= player.y_down():
                    deplacement = 0
                    break
                elif block.y_up() > player.y_down():
                    deplacement = min(deplacement , block.y_up() - player.y_down() - 1)
        return deplacement
    
    
    def check_up_right(self , player : Player , deplacement_up : int , deplacement_right : int) -> tuple:
        deplacement_up = self.check_up(player = player , deplacement = deplacement_up)
        deplacement_right = self.check_right(player = player , deplacement = deplacement_right)
        deplacement_up1 = deplacement_up
        deplacement_right1 = deplacement_right
        for block in player.block_near:
            if player.y-self.__taille_block-deplacement_up+1<=block.y<=player.y-1 and player.x+1<=block.x<=player.x+self.__taille_block+deplacement_right+1:
                #On regarde si x,y est compris dans les coordonnées du bloc avec sa taille
                deplacement_up1=min(deplacement_up1,player.y-self.__taille_block-block.y-1)
                deplacement_right1=min(deplacement_right1,block.x-player.x-self.__taille_block)
        if deplacement_right1 == deplacement_right or deplacement_up1 == deplacement_up:
            return deplacement_up , deplacement_right
        
        if deplacement_right1 > deplacement_up1:
            deplacement_up1 = deplacement_up
            for block in player.block_near:
                if player.y-self.__taille_block-deplacement_up+1<=block.y<=player.y-1 and player.x+1<=block.x<=player.x+self.__taille_block+deplacement_right1+1:
                    #On regarde si x,y est compris dans les coordonnées du bloc avec sa taille
                    deplacement_up1=min(deplacement_up1,player.y-self.__taille_block-block.y-1)
        else:
            deplacement_right1 = deplacement_right
            for block in player.block_near:
                if player.y-self.__taille_block-deplacement_up1+1<=block.y<=player.y-1 and player.x+1<=block.x<=player.x+self.__taille_block+deplacement_right+1:
                    #On regarde si x,y est compris dans les coordonnées du bloc avec sa taille
                    deplacement_right1=min(deplacement_right1,block.x-player.x-self.__taille_block)
        
        
        return deplacement_up1,deplacement_right1
    
    
    def check_up_left(self , player : Player , deplacement_up : int , deplacement_left : int) -> tuple:
        deplacement_up = self.check_up(player = player , deplacement = deplacement_up)
        deplacement_left = self.check_left(player = player , deplacement = deplacement_left)
        deplacement_up1 = deplacement_up
        deplacement_left1 = deplacement_left
        for block in player.block_near:
            if player.y-self.__taille_block-deplacement_up+1<=block.y<=player.y-1 and player.x-self.__taille_block-deplacement_left+1<=block.x<=player.x-1:
                #On regarde si x,y est compris dans les coordonnées du bloc avec sa taille
                deplacement_up1=min(deplacement_up1,player.y-self.__taille_block-block.y-1)
                deplacement_left1=min(deplacement_left1,player.x-block.x-self.__taille_block)
        
        if deplacement_left1 == deplacement_left or deplacement_up1 == deplacement_up:
            return deplacement_up , deplacement_left
        
        if deplacement_left1 > deplacement_up1:
            deplacement_up1 = deplacement_up
            for block in player.block_near:
                if player.y-self.__taille_block-deplacement_up+1<=block.y<=player.y-1 and player.x-self.__taille_block-deplacement_left1+1<=block.x<=player.x-1:
                    #On regarde si x,y est compris dans les coordonnées du bloc avec sa taille
                    deplacement_up1=min(deplacement_up1,player.y-self.__taille_block-block.y-1)
        else:
            deplacement_left1 = deplacement_left
            for block in player.block_near:
                if player.y-self.__taille_block-deplacement_up1+1<=block.y<=player.y-1 and player.x-self.__taille_block-deplacement_left+1<=block.x<=player.x-1:
                    #On regarde si x,y est compris dans les coordonnées du bloc avec sa taille
                    deplacement_left1=min(deplacement_left1,player.x-block.x-self.__taille_block)
        return deplacement_up1,deplacement_left1
    
    
    def check_down_right(self , player : Player , deplacement_down : int , deplacement_right : int) -> tuple:
        deplacement_down = self.check_down(player = player , deplacement = deplacement_down)
        deplacement_right = self.check_right(player = player , deplacement = deplacement_right)
        deplacement_right1 = deplacement_right
        deplacement_down1 = deplacement_down
        for block in player.block_near:
            if player.y+self.__taille_block+1<=block.y<=player.y+2*self.__taille_block+deplacement_down-1 and player.x+1<=block.x<=player.x+self.__taille_block+deplacement_right+1:
                #On regarde si x,y est compris dans les coordonnées du bloc avec sa taille
                deplacement_down1=min(deplacement_down1,block.y-player.y-2*self.__taille_block)
                deplacement_right1=min(deplacement_right1,block.x-player.x-self.__taille_block)
        if deplacement_right1 == deplacement_right or deplacement_down1 == deplacement_down:
            return deplacement_down , deplacement_right
        
        if deplacement_down1 >= deplacement_right1:
            deplacement_right1 = deplacement_right
            for block in player.block_near:
                if player.y+self.__taille_block+1<=block.y<=player.y+2*self.__taille_block+deplacement_down1-1 and player.x+1<=block.x<=player.x+self.__taille_block+deplacement_right+1:
                    #On regarde si x,y est compris dans les coordonnées du bloc avec sa taille
                    deplacement_right1=min(deplacement_right1,block.x-player.x-self.__taille_block)
        else:
            deplacement_down1 = deplacement_down
            for block in player.block_near:
                if player.y+self.__taille_block+1<=block.y<=player.y+2*self.__taille_block+deplacement_down-1 and player.x+1<=block.x<=player.x+self.__taille_block+deplacement_right1+1:
                    #On regarde si x,y est compris dans les coordonnées du bloc avec sa taille
                    deplacement_down1=min(deplacement_down1,block.y-player.y-2*self.__taille_block)
        return deplacement_down1,deplacement_right1
    
    
    def check_down_left(self , player : Player , deplacement_down : int , deplacement_left : int) -> tuple:
        deplacement_down = self.check_down(player = player , deplacement = deplacement_down)
        deplacement_left = self.check_left(player = player , deplacement = deplacement_left)
        deplacement_left1 = deplacement_left
        deplacement_down1 = deplacement_down
        for block in player.block_near:
            if player.y+self.__taille_block+1<=block.y<=player.y+2*self.__taille_block+deplacement_down-1 and player.x-self.__taille_block-deplacement_left+1<=block.x<=player.x-1:
                #On regarde si x,y est compris dans les coordonnées du bloc avec sa taille
                deplacement_down1=min(deplacement_down1,block.y-player.y-2*self.__taille_block)
                deplacement_left1=min(deplacement_left1,player.x-block.x-self.__taille_block)
        
        if deplacement_left1 == deplacement_left or deplacement_down1 == deplacement_down:
            return deplacement_down , deplacement_left
        if deplacement_down1 >= deplacement_left1:
            deplacement_left1 = deplacement_left
            for block in player.block_near:
                if player.y+self.__taille_block+1<=block.y<=player.y+2*self.__taille_block+deplacement_down1-1 and player.x-self.__taille_block-deplacement_left+1<=block.x<=player.x-1:
                    #On regarde si x,y est compris dans les coordonnées du bloc avec sa taille
                    deplacement_left1=min(deplacement_left1,player.x-block.x-self.__taille_block)
        else:
            deplacement_down1 = deplacement_down
            for block in player.block_near:
                if player.y+self.__taille_block+1<=block.y<=player.y+2*self.__taille_block+deplacement_down-1 and player.x-self.__taille_block-deplacement_left1+1<=block.x<=player.x-1:
                    #On regarde si x,y est compris dans les coordonnées du bloc avec sa taille
                    deplacement_down1=min(deplacement_down1,block.y-player.y-2*self.__taille_block)
        return deplacement_down1,deplacement_left1
    
    
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
                    if player.x_left() - 100 <= block.x_left() and block.x_right() <= player.x_right() + 100:
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