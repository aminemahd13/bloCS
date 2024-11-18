


class Block:
    def __init__(self, x : int , y : int , is_solid : bool = True, breakable : bool = True , health : int = 100):
        """
        Initialize a block.
        :params x,y : Representing the block's position.
        :param is_solid: Whether the block can be passed through.
        :param breakable: Whether the block can be broken.
        :param health: The starting health of the block.
        """
        self.x = x
        self.y = y
        self.type = None
        self.is_solid = is_solid
        self.breakable = breakable
        self.health = health

    def take_damage(self , damage : int) -> bool:
        """
        Réduit la vie du bloc.
        Renvoie True si le bloc est cassé, False sinon.
        """
        if self.breakable:
            self.health -= damage
            if self.health <= 0:
                return True
            return False
        return False

    def render(self):
        """
        Affiche le bloc.
        """
        print(f"Rendering block at {(self.x , self.y)}")




class DirtBlock(Block):
    def __init__(self , x : int , y : int):
        super().__init__(x = x , y = y , is_solid = True , breakable = True , health = 50)
        self.type = "Dirt"


class StoneBlock(Block):
    def __init__(self , x : int , y : int):
        super().__init__(x = x , y = y , is_solid = True , breakable = True , health = 200)
        self.type = "Stone"


class WoodBlock(Block):
    def __init__(self , x : int , y : int):
        super().__init__(x = x , y = y , is_solid = True , breakable = True , health = 100)
        self.type = "Wood"


class BedrockBlock(Block):
    def __init__(self , x : int , y : int):
        super().__init__(x = x , y = y , is_solid = True , breakable = False , health = 100)
        self.type = "BedRock"


"""
Utilisation

Initialisation :
wood = WoodBlock(x : int , y : int)
stone = StoneBlock(x : int , y : int)
dirt = DirtBlock(x : int , y : int)
bedrock = BedrockBlock(x : int , y : int)

Attaquer un bloc :
block.take_damage(damage : int) -> bool
Attaque le bloc. Renvoie True si le bloc est détruit, False sinon.

Afficher le bloc :
block.render() -> None
Affiche le bloc

"""