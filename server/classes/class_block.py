from utils.coord_to_screen import coord_to_indice



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
        self.taille = 40
        self.x_indice = x_indice
        self.y_indice = y_indice
        self.x = x_indice * self.taille #Coordonnées en px
        self.y = y_indice * self.taille #Coordonnées en px
        self.type = None
        self.value = None
        self.is_solid = is_solid
        self.breakable = breakable
        self.health = health
        self.drop_item = drop_item
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


class StoneBlock(Block):
    def __init__(self , x_indice : int = None , y_indice : int = None , x : int = None , y : int = None):
        super().__init__(x_indice = x_indice , y_indice = y_indice , x = x , y = y , is_solid = True , breakable = True , health = 400 , tuile_required = 64)
        self.type = "Stone"

class ObsidianBlock(Block):
    def __init__(self , x_indice : int = None , y_indice : int = None , x : int = None , y : int = None):
        super().__init__(x_indice = x_indice , y_indice = y_indice , x = x , y = y , is_solid = True , breakable = True , health = 1200 , tuile_required = 256)
        self.type = "Obsidian"


class WoodBlock(Block):
    def __init__(self , x_indice : int = None , y_indice : int = None , x : int = None , y : int = None):
        super().__init__(x_indice = x_indice , y_indice = y_indice , x = x , y = y , is_solid = True , breakable = True , health = 100)
        self.type = "Wood"


class BedrockBlock(Block):
    def __init__(self , x_indice : int = None , y_indice : int = None , x : int = None , y : int = None):
        super().__init__(x_indice = x_indice , y_indice = y_indice , x = x , y = y , is_solid = True , breakable = True , health = 300 , tuile_required = 0)
        self.type = "Bedrock"
        
class Wood1Block(Block):
    def __init__(self , x_indice : int = None , y_indice : int = None , x : int = None , y : int = None):
        super().__init__(x_indice = x_indice , y_indice = y_indice , x = x , y = y , is_solid = False , breakable = False , health = 100)
        self.type = "Wood1"

class Wood2Block(Block):
    def __init__(self , x_indice : int = None , y_indice : int = None , x : int = None , y : int = None , is_solid = False):
        super().__init__(x_indice = x_indice , y_indice = y_indice , x = x , y = y , is_solid = is_solid , breakable = False , health = 100)
        self.type = "Wood2"
        
class DoorupBlock(Block):
    def __init__(self , x_indice : int = None , y_indice : int = None , x : int = None , y : int = None):
        super().__init__(x_indice = x_indice , y_indice = y_indice , x = x , y = y , is_solid = False , breakable = False , health = 100)
        self.type = "Doorup"
        
class DoordownBlock(Block):
    def __init__(self , x_indice : int = None , y_indice : int = None , x : int = None , y : int = None):
        super().__init__(x_indice = x_indice , y_indice = y_indice , x = x , y = y , is_solid = False , breakable = False , health = 100)
        self.type = "Doordown"
    
    

class TuileBlock(Block):
    def __init__(self, x_indice: int = None, y_indice: int = None, x: int = None, y: int = None, value: int = 2):
        super().__init__(x_indice=x_indice, y_indice=y_indice, x=x, y=y, is_solid=True, breakable=True, health=50)
        self.type = "Tuile"
        self.value = value


class GameBlock(Block):
    def __init__(self, x_indice: int = None, y_indice: int = None, x: int = None, y: int = None):
        super().__init__(x_indice=x_indice, y_indice=y_indice, x=x, y=y, is_solid=False, breakable=False, health=100)
        self.type = "Game"











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