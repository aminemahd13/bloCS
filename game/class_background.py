from class_block import Block, DirtBlock, StoneBlock, WoodBlock, BedrockBlock

def generation_rect_to_pts(liste : list) -> list:
    """
    Renvoie une liste de points en fct des rectangles.
    """
    liste_result = []
    for rect in liste:
        for x in range(rect[0] , rect[2] + 1):
            for y in range(rect[1] , rect[3] + 1):
                liste_result.append([x , y])
    return liste_result



class Background:
    def __init__(self , height : int , width : int):
        self.__height = height
        self.__width = width
        x_spawn = 0 #Indice x en haut à gauche du bloc du spawn
        y_spawn = 0 #Indice y en haut à gauche du bloc du spawn
        self.__taille_block = 40
        self.__dict_block = {}
        liste_dirt = generation_rect_to_pts([])
        liste_dirt_block = []
        for i in range(len(liste_dirt)):
            liste_dirt[i][0] = liste_dirt[i][0] - x_spawn
            liste_dirt[i][0] = liste_dirt[i][0] * self.__taille_block
            liste_dirt[i][1] = liste_dirt[i][1] - y_spawn
            liste_dirt[i][1] = liste_dirt[i][1] * self.__taille_block
            liste_dirt_block.append(DirtBlock(x = liste_dirt[i][0] , y = liste_dirt[i][1]))
        self.__dict_block["Dirt"] = liste_dirt_block

    
     
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
                    return block
        return None
    
    
    def add_block(self , block : Block , decalage_auto : bool = True) -> bool:
        """
        Ajoute un bloc dans le background.
        Renvoie True si le bloc a été placé, False sinon.
        """
        if self.check_block(x = block.x , y = block.y) is None:
            if decalage_auto:
                x = self.__dict_block["Dirt"][0].x
                y = self.__dict_block["Dirt"][0].y
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
                    if liste[i].take_damage(damage = damage):
                        liste.pop(i)
                        return True
                    return False
        return False
    
    
    def render(self) -> None:
        for liste in self.__dict_block.values():
            for block in liste:
                if 1 - self.__taille_block <= block.x <= self.__width and 1 - self.__taille_block <= block.y <= self.__height:
                    block.render()

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



"""