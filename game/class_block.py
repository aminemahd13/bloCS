import pygame

BLOCK_SIZE = 40
class Block:
    def __init__(self, x : int , y : int, is_solid : bool = True, breakable : bool = True , health : int = 100, drop_item: str = None):
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
        self.texture_path = None
        self.drop_item = drop_item
        self.texture = pygame.image.load(self.texture_path)
        self.texture = pygame.transform.scale(self.texture, (BLOCK_SIZE, BLOCK_SIZE))

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



    def render(self, surface):
        if self.texture:  # Ensure texture is loaded
            screen_x = self.x
            screen_y = self.y
            surface.blit(self.texture, (screen_x, screen_y))




class DirtBlock(Block):
    def __init__(self , x : int , y : int, texture):
        super().__init__(x = x , y = y , is_solid = True , breakable = True , health = 50)
        self.type = "Dirt"
        self.texture_path = "/assets/graphics/dirt.png"


class StoneBlock(Block):
    def __init__(self , x : int , y : int, texture):
        super().__init__(x = x , y = y , is_solid = True , breakable = True , health = 200)
        self.type = "Stone"
        self.texture_path = "/assets/graphics/stone.png"


class WoodBlock(Block):
    def __init__(self , x : int , y : int, texture):
        super().__init__(x = x , y = y , is_solid = True , breakable = True , health = 100)
        self.type = "Wood"
        self.texture_path = "/assets/graphics/wood.png"


class BedrockBlock(Block):
    def __init__(self , x : int , y : int):
        super().__init__(x = x , y = y , is_solid = True , breakable = False , health = 100)
        self.type = "Bedrock"
        self.texture_path = "/assets/graphics/bedrock.png"

















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