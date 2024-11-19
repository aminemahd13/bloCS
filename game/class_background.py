from class_block import Block, DirtBlock, StoneBlock, WoodBlock, BedrockBlock, ObsidianBlock
import pygame



 ############# add block is now False make it true



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
        x_spawn = 33 #Indice x en haut à gauche du bloc du spawn
        y_spawn = 6 #Indice y en haut à gauche du bloc du spawn
        self.__taille_block = 40
        self.__dict_block = {} #Dictionnaire contenant tout les blocs
        
        #On ajoute tout les blocs de type Dirt
        liste_dirt = generation_rect_to_pts([(45,15,48,15),(46,16,47,16),(14,11,22,11), (18,7,18,7), (27,13,27,13), (32,13,32,13), (40,18,40,18), (40,15,41,17), (42,15,42,16), (43,15,43,15), (42,13,43,14), (44,12,49,14), (49,11,50,11), (50,12,53,13), (53,14,53,14), (56,11,56,11)])
        liste_dirt_block = []
        for i in range(len(liste_dirt)):
            liste_dirt[i][0] = 2 * liste_dirt[i][0] - 2 * x_spawn - 1
            liste_dirt[i][0] = liste_dirt[i][0] * self.__taille_block // 2
            liste_dirt[i][0] = liste_dirt[i][0] + self.__width // 2
            liste_dirt[i][1] = liste_dirt[i][1] - y_spawn - 1
            liste_dirt[i][1] = liste_dirt[i][1] * self.__taille_block
            liste_dirt[i][1] = liste_dirt[i][1] + self.__height // 2
            liste_dirt_block.append(DirtBlock(x = liste_dirt[i][0] , y = liste_dirt[i][1]))
        self.__dict_block["Dirt"] = liste_dirt_block

        #On ajoute tout les blocs de type Stone
        liste_stone = generation_rect_to_pts([(45,25,45,25),(71,15,71,15),(63,22,64,22),(45,20,45,20), (46,24,47,25), (48,25,49,25), (49,22,52,22), (50,23,54,23), (51,24,59,24), (55,25,60,25), (58,22,58,22), (59,18,63,18), (63,21,66,21), (65,22,70,22), (68,23,72,24), (73,24,73,24), (65,16,67,16), (71,16,71,16), (72,15,73,16), (73,18,74,18), (73,20,73,21)])
        liste_stone_block = []
        for i in range(len(liste_stone)):
            liste_stone[i][0] = 2 * liste_stone[i][0] - 2 * x_spawn - 1
            liste_stone[i][0] = liste_stone[i][0] * self.__taille_block // 2
            liste_stone[i][0] = liste_stone[i][0] + self.__width // 2
            liste_stone[i][1] = liste_stone[i][1] - y_spawn - 1
            liste_stone[i][1] = liste_stone[i][1] * self.__taille_block
            liste_stone[i][1] = liste_stone[i][1] + self.__height // 2
            liste_stone_block.append(StoneBlock(x = liste_stone[i][0] , y = liste_stone[i][1]))
        self.__dict_block["Stone"] = liste_stone_block
        
        #On ajoute tout les blocs de type Obsidian
        liste_obsidian = generation_rect_to_pts([(23,21,28,21),(10,17,10,17), (11,18,11,18), (11,16,12,17), (13,16,13,16), (12,15,21,15), (13,14,19,14), (19,16,26,16), (21,17,26,17), (11,20,11,20), (10,21,13,21), (9,22,15,22), (13,23,23,23), (16,24,22,24), (22,22,27,22), (23,22,28,22), (27,20,28,20), (28,19,28,19)])
        liste_obsidian_block = []
        for i in range(len(liste_obsidian)):
            liste_obsidian[i][0] = 2 * liste_obsidian[i][0] - 2 * x_spawn - 1
            liste_obsidian[i][0] = liste_obsidian[i][0] * self.__taille_block // 2
            liste_obsidian[i][0] = liste_obsidian[i][0] + self.__width // 2
            liste_obsidian[i][1] = liste_obsidian[i][1] - y_spawn - 1
            liste_obsidian[i][1] = liste_obsidian[i][1] * self.__taille_block
            liste_obsidian[i][1] = liste_obsidian[i][1] + self.__height // 2
            liste_obsidian_block.append(ObsidianBlock(x = liste_obsidian[i][0] , y = liste_obsidian[i][1]))
        self.__dict_block["Obsidian"] = liste_obsidian_block
        
        #On ajoute tout les blocs de type Wood
        liste_wood = generation_rect_to_pts([])
        liste_wood_block = []
        for i in range(len(liste_wood)):
            liste_wood[i][0] = 2 * liste_wood[i][0] - 2 * x_spawn - 1
            liste_wood[i][0] = liste_wood[i][0] * self.__taille_block // 2
            liste_wood[i][0] = liste_wood[i][0] + self.__width // 2
            liste_wood[i][1] = liste_wood[i][1] - y_spawn - 1
            liste_wood[i][1] = liste_wood[i][1] * self.__taille_block
            liste_wood[i][1] = liste_wood[i][1] + self.__height // 2
            liste_wood_block.append(WoodBlock(x = liste_wood[i][0] , y = liste_wood[i][1]))
        self.__dict_block["Wood"] = liste_wood_block

        #On ajoute tout les blocs de type Bedrock
        liste_bedrock = generation_rect_to_pts([(27,19,27,19),(0,3,1,3), (4,3,14,3), (8,2,12,2), (0,4,13,8), (14,4,14,7),(14,4,14,7), (15,4,15,6), (16,5,16,5), (0,9,8,9), (0,10,5,10), (0,11,2,11), (16,9,16,9), (0,14,3,14), (0,15,4,26), (5,16,5,20), (6,18,6,20), (7,20,7,20), (5,25,45,26), (5,23,12,24), (13,24,15,24), (23,24,36,24), (24,23,35,23), (28,22,34,22), (29,21,33,21), (29,20,31,20), (29,19,30,19), (10,20,10,20), (11,19,11,19), (12,18,26,20), (14,16,18,16), (13,17,20,17), (14,21,22,21), (16,22,21,22), (9,17,9,17), (9,16,10,16), (8,15,11,15), (7,14,12,14), (6,13,26,13), (8,12,23,12), (20,14,27,14), (22,15,28,15), (27,16,28,16), (27,17,29,17), (27,18,29,18), (27,27,27,29), (20,2,25,2), (19,3,25,3), (19,4,26,4), (20,5,27,5), (19,6,30,6), (19,7,31,7), (18,8,20,8), (46,7,47,7), (51,7,67,7), (55,6,59,6), (55,5,57,5), (64,6,66,6), (31,8,68,8), (36,9,69,9), (33,10,69,10), (36,11,48,11), (51,11,55,11), (60,11,69,11), (63,12,64,12), (38,12,41,14), (42,12,43,12), (30,13,31,13), (33,13,34,13), (30,14,35,14), (31,15,39,15), (34,16,39,16), (35,17,39,17), (38,18,39,18), (39,19,47,19), (42,20,44,20), (46,20,46,20), (41,18,49,18), (42,17,53,17), (43,16,45,16), (44,15,44,15), (48,16,54,16), (49,15,55,15), (50,14,52,14), (40,24,44,24), (46,23,49,23), (48,24,50,24), (50,25,54,25), (46,26,76,26), (52,20,53,20), (51,21,56,21), (53,22,57,22), (59,22,61,22), (55,23,67,23), (63,22,64,22), (60,24,67,24), (61,25,76,25), (74,24,76,24), (73,23,76,23), (71,22,76,22), (67,21,72,21), (74,21,76,21), (63,20,72,20), (75,20,76,20), (58,19,70,19), (76,19,76,19), (64,18,65,18), (68,18,69,18), (75,18,76,18), (72,17,77,17), (74,16,76,16), (65,15,71,15), (74,15,76,15), (66,14,76,14), (68,13,75,13), (71,12,75,12), (72,11,74,11), (73,10,73,10), (57,16,61,16), (57,15,60,15), (58,14,59,14)])
        liste_bedrock_block = []
        enlever_bedrock=[[27,27],[27,28],[27,29],[45,25],[71,15],[63,22],[64,22],[77,17]]
        for i in range(len(liste_bedrock)):
            if liste_bedrock[i] not in enlever_bedrock:
                liste_bedrock[i][0] = 2 * liste_bedrock[i][0] - 2 * x_spawn - 1
                liste_bedrock[i][0] = liste_bedrock[i][0] * self.__taille_block // 2
                liste_bedrock[i][0] = liste_bedrock[i][0] + self.__width // 2
                liste_bedrock[i][1] = liste_bedrock[i][1] - y_spawn - 1
                liste_bedrock[i][1] = liste_bedrock[i][1] * self.__taille_block
                liste_bedrock[i][1] = liste_bedrock[i][1] + self.__height // 2
                liste_bedrock_block.append(BedrockBlock(x = liste_bedrock[i][0] , y = liste_bedrock[i][1]))
        self.__dict_block["Bedrock"] = liste_bedrock_block
    
     
    def right(self , deplacement : int) -> None:
        """
        Déplace tout les blocs sur la gauche.
        """
        for liste in self.__dict_block.values():
            for block in liste:
                block.x = block.x - deplacement
    
    
    def left(self , deplacement : int) -> None:
        """
        Déplace tout les blocs sur la droite.
        """
        for liste in self.__dict_block.values():
            for block in liste:
                block.x = block.x + deplacement
    
    
    def up(self , deplacement : int) -> None:
        """
        Déplace tout les blocs sur le bas.
        """
        for liste in self.__dict_block.values():
            for block in liste:
                block.y = block.y + deplacement
    
    
    def down(self , deplacement : int) -> None:
        """
        Déplace tout les blocs sur le haut.
        """
        for liste in self.__dict_block.values():
            for block in liste:
                block.y = block.y - deplacement
    
    
    def check_block(self , x : int , y : int) -> Block:
        """
        Renvoie le bloc en x , y.
        """
        for liste in self.__dict_block.values():
            for block in liste:
                if block.x <= x < block.x + self.__taille_block and block.y <= y < block.y + self.__taille_block:
                    #On regarde si x,y est compris dans les coordonnées du bloc avec sa taille
                    return block
        return None
    
    
    def add_block(self , block : Block , decalage_auto : bool = False) -> bool:
        """
        Ajoute un bloc dans le background.
        Renvoie True si le bloc a été placé, False sinon.
        """
        if self.check_block(x = block.x , y = block.y) is None:
            if decalage_auto: #Ajustement automatique
                x = self.__dict_block["Bedrock"][0].x
                y = self.__dict_block["Bedrock"][0].y
                while x < block.x:
                    x += self.__taille_block
                while x > block.x:
                    x -= self.__taille_block
                while y < block.y:
                    y += self.__taille_block
                while y > block.y:
                    y -= self.__taille_block
                block.x = x
                block.y = y
            self.__dict_block[block.type].append(block)
            return True
        return False
    
    
    def damage_block(self , x : int , y : int , damage : int) -> bool:
        """
        Attaque le bloc se situant en x , y.
        S'il y avait un bloc qui a été détruit, renvoie True.
        Sinon, renvoie False.
        """
        for liste in self.__dict_block.values():
            for i in range(len(liste)):
                if liste[i].x <= x < liste[i].x + self.__taille_block and liste[i].y <= y < liste[i].y + self.__taille_block:
                    #On regarde si x,y est compris dans les coordonnées du bloc avec sa taille
                    if liste[i].take_damage(damage = damage):
                        liste.pop(i)
                        return True
                    return False
        return False
    
    
    def check_right(self , x_player : int , y_player : int , deplacement : int) -> int:
        """
        Renvoie le déplacement maximal pouvant être effectué sur la droite,
        inférieur à déplacement.
        """
        for x in range(deplacement):
            for y in range(2 * self.__taille_block):
                block = self.check_block(x = x_player + self.__taille_block + x , y = y_player + y)
                if block is not None:
                    return x
        return deplacement
    
    
    def check_left(self , x_player : int , y_player : int , deplacement : int) -> int:
        """
        Renvoie le déplacement maximal pouvant être effectué sur la gauche,
        inférieur à déplacement.
        """
        for x in range(deplacement):
            for y in range(2 * self.__taille_block):
                block = self.check_block(x = x_player - 1 - x , y = y_player + y)
                if block is not None:
                    return x
        return deplacement
    
    
    def check_up(self , x_player : int , y_player : int , deplacement : int) -> int:
        """
        Renvoie le déplacement maximal pouvant être effectué vers le haut,
        inférieur à déplacement.
        """
        for y in range(deplacement):
            for x in range(self.__taille_block):
                block = self.check_block(x = x_player + x , y = y_player - 1 - y)
                if block is not None:
                    return y
        return deplacement
    
    
    def check_down(self , x_player : int , y_player : int , deplacement : int) -> int:
        """
        Renvoie le déplacement maximal pouvant être effectué vers le bas,
        inférieur à déplacement.
        """
        for y in range(deplacement):
            for x in range(self.__taille_block):
                block = self.check_block(x = x_player + x , y = y_player + 2 * self.__taille_block + y)
                if block is not None:
                    return y
        return deplacement
    
    
    def check_up_left(self , x_player : int , y_player : int , deplacement_up : int , deplacement_left : int) -> tuple:
        """
        Renvoie le déplacement maximal pouvant être effectué vers le haut et vers la gauche,
        inférieur à déplacement.
        """
        deplacement_up_max1 = self.check_up(x_player = x_player , y_player = y_player , deplacement = deplacement_up)
        deplacement_left_max1 = self.check_left(x_player = x_player , y_player = y_player , deplacement = deplacement_left)
        
        if deplacement_up_max1 == 0 or deplacement_left_max1 == 0:
            return deplacement_up_max1 , deplacement_left_max1
        
        deplacement_left_max2 = None
        for x in range(deplacement_left_max1):
            for y in range(2 * self.__taille_block + deplacement_up_max1):
                block = self.check_block(x = x_player - 1 - x , y = y_player + 2 * self.__taille_block - 1 - y)
                if block is not None:
                    deplacement_left_max2 = x
                    break
            if deplacement_left_max2 is not None:
                break
        if deplacement_left_max2 is None:
            deplacement_left_max2 = deplacement_left_max1
        
        deplacement_up_max2 = None
        for y in range(deplacement_up_max1):
            for x in range(self.__taille_block + deplacement_left_max1):
                block = self.check_block(x = x_player - 1 - x , y = y_player - 1 - y)
                if block is not None:
                    deplacement_up_max2 = y
                    break
            if deplacement_up_max2 is not None:
                break
        if deplacement_up_max2 is None:
            deplacement_up_max2 = deplacement_up_max1
        
        if deplacement_left_max2 >= deplacement_up_max2:
            if deplacement_left_max1 == deplacement_left_max2:
                return deplacement_up_max2 , deplacement_left_max2
            deplacement_up_max3 = None
            for y in range(deplacement_up_max2):
                for x in range(self.__taille_block + deplacement_left_max2):
                    block = self.check_block(x = x_player - 1 - x , y = y_player - 1 - y)
                    if block is not None:
                        deplacement_up_max3 = y
                        break
                if deplacement_up_max3 is not None:
                    break
            if deplacement_up_max3 is None:
                deplacement_up_max3 = deplacement_up_max2
            return deplacement_up_max3 , deplacement_left_max2
        
        else:
            if deplacement_up_max1 == deplacement_up_max2:
                return deplacement_up_max2 , deplacement_left_max2
            deplacement_left_max3 = None
            for x in range(deplacement_left_max2):
                for y in range(2 * self.__taille_block + deplacement_up_max2):
                    block = self.check_block(x = x_player - 1 - x , y = y_player + 2 * self.__taille_block - 1 - y)
                    if block is not None:
                        deplacement_left_max3 = x
                        break
                if deplacement_left_max3 is not None:
                    break
            if deplacement_left_max3 is None:
                deplacement_left_max3 = deplacement_left_max1
            return deplacement_up_max2 , deplacement_left_max3
    
    
    def check_up_right(self , x_player : int , y_player : int , deplacement_up : int , deplacement_right : int) -> tuple:
        """
        Renvoie le déplacement maximal pouvant être effectué vers le haut et vers la droite,
        inférieur à déplacement.
        """
        deplacement_up_max1 = self.check_up(x_player = x_player , y_player = y_player , deplacement = deplacement_up)
        deplacement_right_max1 = self.check_right(x_player = x_player , y_player = y_player , deplacement = deplacement_right)
        
        if deplacement_up_max1 == 0 or deplacement_right_max1 == 0:
            return deplacement_up_max1 , deplacement_right_max1
        
        deplacement_right_max2 = None
        for x in range(deplacement_right_max1):
            for y in range(2 * self.__taille_block + deplacement_up_max1):
                block = self.check_block(x = x_player + self.__taille_block + x , y = y_player + 2 * self.__taille_block - 1 - y)
                if block is not None:
                    deplacement_right_max2 = x
                    break
            if deplacement_right_max2 is not None:
                break
        if deplacement_right_max2 is None:
            deplacement_right_max2 = deplacement_right_max1
        
        deplacement_up_max2 = None
        for y in range(deplacement_up_max1):
            for x in range(self.__taille_block + deplacement_right_max1):
                block = self.check_block(x = x_player + x , y = y_player - 1 - y)
                if block is not None:
                    deplacement_up_max2 = y
                    break
            if deplacement_up_max2 is not None:
                break
        if deplacement_up_max2 is None:
            deplacement_up_max2 = deplacement_up_max1
        
        if deplacement_right_max2 >= deplacement_up_max2:
            if deplacement_right_max1 == deplacement_right_max2:
                return deplacement_up_max2 , deplacement_right_max2
            deplacement_up_max3 = None
            for y in range(deplacement_up_max2):
                for x in range(self.__taille_block + deplacement_right_max2):
                    block = self.check_block(x = x_player + x , y = y_player - 1 - y)
                    if block is not None:
                        deplacement_up_max3 = y
                        break
                if deplacement_up_max3 is not None:
                    break
            if deplacement_up_max3 is None:
                deplacement_up_max3 = deplacement_up_max2
            return deplacement_up_max3 , deplacement_right_max2
        
        else:
            if deplacement_up_max1 == deplacement_up_max2:
                return deplacement_up_max2 , deplacement_right_max2
            deplacement_right_max3 = None
            for x in range(deplacement_right_max2):
                for y in range(2 * self.__taille_block + deplacement_up_max2):
                    block = self.check_block(x = x_player + self.__taille_block + x , y = y_player + 2 * self.__taille_block - 1 - y)
                    if block is not None:
                        deplacement_right_max3 = x
                        break
                if deplacement_right_max3 is not None:
                    break
            if deplacement_right_max3 is None:
                deplacement_right_max3 = deplacement_right_max1
            return deplacement_up_max2 , deplacement_right_max3
    
    
    def check_down_left(self , x_player : int , y_player : int , deplacement_down : int , deplacement_left : int) -> tuple:
        """
        Renvoie le déplacement maximal pouvant être effectué vers le haut et vers la gauche,
        inférieur à déplacement.
        """
        deplacement_down_max1 = self.check_down(x_player = x_player , y_player = y_player , deplacement = deplacement_down)
        deplacement_left_max1 = self.check_left(x_player = x_player , y_player = y_player , deplacement = deplacement_left)
        
        if deplacement_down_max1 == 0 or deplacement_left_max1 == 0:
            return deplacement_down_max1 , deplacement_left_max1
        
        deplacement_left_max2 = None
        for x in range(deplacement_left_max1):
            for y in range(2 * self.__taille_block + deplacement_down_max1):
                block = self.check_block(x = x_player - 1 - x , y = y_player +  y)
                if block is not None:
                    deplacement_left_max2 = x
                    break
            if deplacement_left_max2 is not None:
                break
        if deplacement_left_max2 is None:
            deplacement_left_max2 = deplacement_left_max1
        
        deplacement_down_max2 = None
        for y in range(deplacement_down_max1):
            for x in range(self.__taille_block + deplacement_left_max1):
                block = self.check_block(x = x_player - 1 - x , y = y_player + 2 * self.__taille_block + y)
                if block is not None:
                    deplacement_down_max2 = y
                    break
            if deplacement_down_max2 is not None:
                break
        if deplacement_down_max2 is None:
            deplacement_down_max2 = deplacement_down_max1
        
        if deplacement_left_max2 >= deplacement_down_max2:
            if deplacement_left_max1 == deplacement_left_max2:
                return deplacement_down_max2 , deplacement_left_max2
            deplacement_down_max3 = None
            for y in range(deplacement_down_max2):
                for x in range(self.__taille_block + deplacement_left_max2):
                    block = self.check_block(x = x_player - 1 - x , y = y_player + 2 * self.__taille_block + y)
                    if block is not None:
                        deplacement_down_max3 = y
                        break
                if deplacement_down_max3 is not None:
                    break
            if deplacement_down_max3 is None:
                deplacement_down_max3 = deplacement_down_max2
            return deplacement_down_max3 , deplacement_left_max2
        
        else:
            if deplacement_down_max1 == deplacement_down_max2:
                return deplacement_down_max2 , deplacement_left_max2
            deplacement_left_max3 = None
            for x in range(deplacement_left_max2):
                for y in range(2 * self.__taille_block + deplacement_down_max2):
                    block = self.check_block(x = x_player - 1 - x , y = y_player + y)
                    if block is not None:
                        deplacement_left_max3 = x
                        break
                if deplacement_left_max3 is not None:
                    break
            if deplacement_left_max3 is None:
                deplacement_left_max3 = deplacement_left_max1
            return deplacement_down_max2 , deplacement_left_max3
    
    
    def check_down_right(self , x_player : int , y_player : int , deplacement_down : int , deplacement_right : int) -> tuple:
        """
        Renvoie le déplacement maximal pouvant être effectué vers le bas et vers la droite,
        inférieur à déplacement.
        """
        deplacement_down_max1 = self.check_up(x_player = x_player , y_player = y_player , deplacement = deplacement_down)
        deplacement_right_max1 = self.check_right(x_player = x_player , y_player = y_player , deplacement = deplacement_right)
        
        if deplacement_down_max1 == 0 or deplacement_right_max1 == 0:
            return deplacement_down_max1 , deplacement_right_max1
        
        deplacement_right_max2 = None
        for x in range(deplacement_right_max1):
            for y in range(2 * self.__taille_block + deplacement_down_max1):
                block = self.check_block(x = x_player + self.__taille_block + x , y = y_player + y)
                if block is not None:
                    deplacement_right_max2 = x
                    break
            if deplacement_right_max2 is not None:
                break
        if deplacement_right_max2 is None:
            deplacement_right_max2 = deplacement_right_max1
        
        deplacement_down_max2 = None
        for y in range(deplacement_down_max1):
            for x in range(self.__taille_block + deplacement_right_max1):
                block = self.check_block(x = x_player + x , y = y_player + 2 * self.__taille_block + y)
                if block is not None:
                    deplacement_down_max2 = y
                    break
            if deplacement_down_max2 is not None:
                break
        if deplacement_down_max2 is None:
            deplacement_down_max2 = deplacement_down_max1
        
        if deplacement_right_max2 >= deplacement_down_max2:
            if deplacement_right_max1 == deplacement_right_max2:
                return deplacement_down_max2 , deplacement_right_max2
            deplacement_down_max3 = None
            for y in range(deplacement_down_max2):
                for x in range(self.__taille_block + deplacement_right_max2):
                    block = self.check_block(x = x_player + x , y = y_player + 2 * self.__taille_block + y)
                    if block is not None:
                        deplacement_down_max3 = y
                        break
                if deplacement_down_max3 is not None:
                    break
            if deplacement_down_max3 is None:
                deplacement_down_max3 = deplacement_down_max2
            return deplacement_down_max3 , deplacement_right_max2
        
        else:
            if deplacement_down_max1 == deplacement_down_max2:
                return deplacement_down_max2 , deplacement_right_max2
            deplacement_right_max3 = None
            for x in range(deplacement_right_max2):
                for y in range(2 * self.__taille_block + deplacement_down_max2):
                    block = self.check_block(x = x_player + self.__taille_block + x , y = y_player + y)
                    if block is not None:
                        deplacement_right_max3 = x
                        break
                if deplacement_right_max3 is not None:
                    break
            if deplacement_right_max3 is None:
                deplacement_right_max3 = deplacement_right_max1
            return deplacement_down_max2 , deplacement_right_max3
    
    
    def render(self, screen) -> None:
        """
        Affiche le background.
        """
        for liste in self.__dict_block.values():
            for block in liste:
                if 1 - self.__taille_block <= block.x <= self.__width and 1 - self.__taille_block <= block.y <= self.__height:
                    #On affiche uniquement les blocs qui se situent dans la map
                    block.render(screen)

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