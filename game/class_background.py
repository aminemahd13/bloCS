from class_block import Block, DirtBlock

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
    def __init__(self):
        x_spawn = 0 #Indice x du block en haut à gauche lors du spawn
        y_spawn = 0 #Indice y du block en haut à gauche lors du spawn
        self.deplacement = 4 #Deplacement en px à chaque boucle
        self.taille_block = 40
        self.dict_coord = {}
        self.dict_block = {}
        liste_dirt = generation_rect_to_pts([])
        liste_dirt_block = []
        for i in range(len(liste_dirt)):
            liste_dirt[i][0] = liste_dirt[i][0] - x_spawn
            liste_dirt[i][0] = liste_dirt[i][0] * self.taille_block
            liste_dirt[i][1] = liste_dirt[i][1] - y_spawn
            liste_dirt[i][1] = liste_dirt[i][1] * self.taille_block
            liste_dirt_block.append(DirtBlock(x = liste_dirt[i][0] , y = liste_dirt[i][1]))
        self.dict_coord["Dirt"] = liste_dirt
        self.dict_block["Dirt"] = liste_dirt_block
        
        
    def right(self) -> None:
        """
        Déplace tout les blocs sur la gauche.
        """
        for liste in self.dict_block.values():
            for block in liste:
                block.x = block.x - self.deplacement
        for liste in self.dict_coord.values():
            for block in liste:
                block[0] = block[0] - self.deplacement
    
    def left(self) -> None:
        """
        Déplace tout les blocs sur la droite.
        """
        for liste in self.dict_block.values():
            for block in liste:
                block.x = block.x + self.deplacement
        for liste in self.dict_coord.values():
            for block in liste:
                block[0] = block[0] + self.deplacement
    
    def up(self) -> None:
        """
        Déplace tout les blocs sur le bas.
        """
        for liste in self.dict_block.values():
            for block in liste:
                block.y = block.y + self.deplacement
        for liste in self.dict_coord.values():
            for block in liste:
                block[1] = block[1] + self.deplacement
    
    def down(self) -> None:
        """
        Déplace tout les blocs sur le haut.
        """
        for liste in self.dict_block.values():
            for block in liste:
                block.y = block.y - self.deplacement
        for liste in self.dict_coord.values():
            for block in liste:
                block[1] = block[1] - self.deplacement
    
    def check_block(self , x : int , y : int) -> str:
        """
        Renvoie le type du block en x , y.
        """
        for cle , liste in self.dict_coord.items():
            for block in liste:
                if block[0] <= x < block[0] + self.taille_block and block[1] <= y < block[0] + self.taille_block:
                    return cle
        return None
    
    def add_block(self , block : Block) -> None:
        """
        Ajoute un block dans le background
        """
        