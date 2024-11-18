from class_block import DirtBlock

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
        taille_block = 40
        self.dict = {}
        liste_dirt = generation_rect_to_pts([])
        for i in range(len(liste_dirt)):
            liste_dirt[i][0] = liste_dirt[i][0] - x_spawn
            liste_dirt[i][0] = liste_dirt[i][0] * taille_block
            liste_dirt[i][1] = liste_dirt[i][1] - y_spawn
            liste_dirt[i][1] = liste_dirt[i][1] * taille_block
            liste_dirt[i] = DirtBlock(position = liste_dirt[i])
        self.dict["Dirt"] = liste_dirt
        
    def droite(self) -> None:
        """
        Déplace tout les blocs sur la gauche.
        """
        for list in self.dict.values():
            for block in list:
                block.x = block.x - self.deplacement
    
    def gauche(self) -> None:
        """
        Déplace tout les blocs sur la droite.
        """
        for list in self.dict.values():
            for block in list:
                block.x = block.x + self.deplacement
    
    def haut(self) -> None:
        """
        Déplace tout les blocs sur le bas.
        """
        for list in self.dict.values():
            for block in list:
                block.y = block.y + self.deplacement
    
    def bas(self) -> None:
        """
        Déplace tout les blocs sur le haut.
        """
        for list in self.dict.values():
            for block in list:
                block.y = block.y - self.deplacement