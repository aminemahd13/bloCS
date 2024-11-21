import pygame
from utils.coord_to_screen import coord_to_screen, coord_to_indice

class Block:
    def __init__(self , is_solid : bool = True, breakable : bool = True , health : int = 100, drop_item: str = None , x_indice : int = None , y_indice : int = None , x : int = None , y : int = None , tuile_required : int = 0):
        """
        Initialize a block.
        :params x_indice , y_indice : Representing the block's position in the map.
        :param is_solid: Whether the block can be passed through.
        :param breakable: Whether the block can be broken.
        :param health: The starting health of the block.
        """
        if x_indice is None:
            x_indice , y_indice = coord_to_indice(x = x , y = y)
        self.add_background = False
        self.taille = 40
        self.x_indice = x_indice
        self.y_indice = y_indice
        self.x = x_indice * self.taille #Coordonnées en px
        self.y = y_indice * self.taille #Coordonnées en px
        self.type = None
        self.is_solid = is_solid
        self.breakable = breakable
        self.health = health
        self.drop_item = drop_item
        self.texture = None
        self.texture_path = None
        self.tuile_required = tuile_required

    def take_damage(self , damage : int , tuile_max : int) -> bool:
        """
        Réduit la vie du bloc.
        Renvoie True si le bloc est cassé, False sinon.
        """
        if self.breakable and tuile_max >= self.tuile_required:
            self.health -= damage
            if self.health <= 0:
                return True
            return False
        return False



    def render(self, screen , player) -> None:
        """
        Affiche le bloc sur l'écran du joueur.
        """
        if self.texture:  # Ensure texture is loaded
            x_screen , y_screen = coord_to_screen(x = self.x , y = self.y , player = player)
            screen.blit(self.texture, (x_screen , y_screen))
    
    
    def y_up(self):
        """
        Coordonnée y en haut.
        """
        return self.y
    
    def y_down(self):
        """
        Coordonnée y en bas.
        """
        return self.y + self.taille - 1
    
    def x_left(self):
        """
        Coordonnée x à gauche.
        """
        return self.x
    
    def x_right(self):
        """
        Coordonnée x à droite.
        """
        return self.x + self.taille - 1


class DirtBlock(Block):
    def __init__(self , x_indice : int = None , y_indice : int = None , x : int = None , y : int = None):
        super().__init__(x_indice = x_indice , y_indice = y_indice , x = x , y = y , is_solid = True , breakable = True , health = 50 , tuile_required = 16)
        self.type = "Dirt"
        self.texture_path = "assets/graphics/dirt.png"
        self.texture = pygame.image.load(self.texture_path)
        self.texture = pygame.transform.scale(self.texture, (self.taille , self.taille))


class StoneBlock(Block):
    def __init__(self , x_indice : int = None , y_indice : int = None , x : int = None , y : int = None):
        super().__init__(x_indice = x_indice , y_indice = y_indice , x = x , y = y , is_solid = True , breakable = True , health = 400 , tuile_required = 64)
        self.type = "Stone"
        self.texture_path = "assets/graphics/stone.png"
        self.texture = pygame.image.load(self.texture_path)
        self.texture = pygame.transform.scale(self.texture, (self.taille, self.taille))

class ObsidianBlock(Block):
    def __init__(self , x_indice : int = None , y_indice : int = None , x : int = None , y : int = None):
        super().__init__(x_indice = x_indice , y_indice = y_indice , x = x , y = y , is_solid = True , breakable = True , health = 1200 , tuile_required = 256)
        self.type = "Obsidian"
        self.texture_path = "assets/graphics/obsidian.png"
        self.texture = pygame.image.load(self.texture_path)
        self.texture = pygame.transform.scale(self.texture, (self.taille, self.taille))


class WoodBlock(Block):
    def __init__(self , x_indice : int = None , y_indice : int = None , x : int = None , y : int = None):
        super().__init__(x_indice = x_indice , y_indice = y_indice , x = x , y = y , is_solid = True , breakable = True , health = 100)
        self.type = "Wood"
        self.texture_path = "assets/graphics/dirt.png"
        self.texture = pygame.image.load(self.texture_path)
        self.texture = pygame.transform.scale(self.texture, (self.taille, self.taille))



class BedrockBlock(Block):
    def __init__(self , x_indice : int = None , y_indice : int = None , x : int = None , y : int = None):
        super().__init__(x_indice = x_indice , y_indice = y_indice , x = x , y = y , is_solid = True , breakable = True , health = 300 , tuile_required = 0)
        self.type = "Bedrock"
        self.texture_path = "assets/graphics/bedrock.png"
        self.texture = pygame.image.load(self.texture_path)
        self.texture = pygame.transform.scale(self.texture, (self.taille, self.taille))
        
class Wood1Block(Block):
    def __init__(self , x_indice : int = None , y_indice : int = None , x : int = None , y : int = None):
        super().__init__(x_indice = x_indice , y_indice = y_indice , x = x , y = y , is_solid = False , breakable = False , health = 100)
        self.type = "Wood1"
        self.texture_path = "assets/graphics/wood1.png"
        self.texture = pygame.image.load(self.texture_path)
        self.texture = pygame.transform.scale(self.texture, (self.taille, self.taille))

class Wood2Block(Block):
    def __init__(self , x_indice : int = None , y_indice : int = None , x : int = None , y : int = None , is_solid = False):
        super().__init__(x_indice = x_indice , y_indice = y_indice , x = x , y = y , is_solid = is_solid , breakable = False , health = 100)
        self.type = "Wood2"
        self.texture_path = "assets/graphics/wood2.png"
        self.texture = pygame.image.load(self.texture_path)
        self.texture = pygame.transform.scale(self.texture, (self.taille, self.taille))
        
class DoorupBlock(Block):
    def __init__(self , x_indice : int = None , y_indice : int = None , x : int = None , y : int = None):
        super().__init__(x_indice = x_indice , y_indice = y_indice , x = x , y = y , is_solid = False , breakable = False , health = 100)
        self.taille
        self.type = "Doorup"
        self.texture_path = "assets/graphics/porteup.png"
        self.texture = pygame.image.load(self.texture_path)
        self.texture = pygame.transform.scale(self.texture, (self.taille, self.taille))
        
class DoordownBlock(Block):
    def __init__(self , x_indice : int = None , y_indice : int = None , x : int = None , y : int = None):
        super().__init__(x_indice = x_indice , y_indice = y_indice , x = x , y = y , is_solid = False , breakable = False , health = 100)
        self.taille
        self.type = "Doordown"
        self.texture_path = "assets/graphics/portedown.png"
        self.texture = pygame.image.load(self.texture_path)
        self.texture = pygame.transform.scale(self.texture, (self.taille, self.taille))
    
    

class TuileBlock(Block):
    def __init__(self , x_indice : int = None , y_indice : int = None , x : int = None , y : int = None, value : int = 2):
        super().__init__(x_indice = x_indice , y_indice = y_indice , x = x , y = y , is_solid = True , breakable = True , health = 100)
        self.value = value
        if value in [8,16]:
            self.tuile_required = 16
        elif value in [32,64]:
            self.tuile_required = 64
        elif value in [128,256,512]:
            self.tuile_required = 256
        self.type = "Tuile"
        self.texture_path = "assets/graphics/tuile_" + str(value) + ".png"
        self.texture = pygame.image.load(self.texture_path)
        self.texture = pygame.transform.scale(self.texture, (self.taille, self.taille))


class GameBlock(Block):
    def __init__(self , x_indice : int = None , y_indice : int = None , x : int = None , y : int = None):
        super().__init__(x_indice = x_indice , y_indice = y_indice , x = x , y = y , is_solid = True , breakable = False , health = 100)
        self.type = "Game"
        #self.texture_path = "assets/graphics/2048/" + str(value) + ".png"
        self.texture_path = "assets/graphics/bloc_2048.png"
        self.texture = pygame.image.load(self.texture_path)
        self.texture = pygame.transform.scale(self.texture, (self.taille, self.taille))











"""
Utilisation

Initialisation :
wood = WoodBlock(x : int , y : int)
stone = StoneBlock(x :  , y : int
dirt = DirtBlock(x : int , y : int)
bedrock = BedrockBlock(x : int , y : int)

Attaquer un bloc :
block.take_damage(damage : int) -> bool
Attaque le bloc. Renvoie True si le bloc est détruit, False sinon.

Afficher le bloc :
block.render() -> None
Affiche le bloc

"""