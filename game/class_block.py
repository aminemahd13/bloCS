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
        self.texture = None
        self.drop_item = drop_item

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

    def _load_texture(self):
        if self.texture_path:
            self.texture = pygame.image.load(self.texture_path)
            self.texture = pygame.transform.scale(self.texture, (BLOCK_SIZE, BLOCK_SIZE))


    def render(self, surface):
        if self.texture:  # Ensure texture is loaded
            screen_x = self.x
            screen_y = self.y
            surface.blit(self.texture, (screen_x, screen_y))




class DirtBlock(Block):
    def __init__(self , x : int , y : int, texture):
        super().__init__(x = x , y = y , is_solid = True , breakable = True , health = 50)
        self.type = "Dirt"
        self.texture_path = texture


class StoneBlock(Block):
    def __init__(self , x : int , y : int, texture):
        super().__init__(x = x , y = y , is_solid = True , breakable = True , health = 200)
        self.type = "Stone"
        self.texture_path = texture


class WoodBlock(Block):
    def __init__(self , x : int , y : int, texture):
        super().__init__(x = x , y = y , is_solid = True , breakable = True , health = 100)
        self.type = "Wood"
        self.texture_path = texture


class BedrockBlock(Block):
    def __init__(self , x : int , y : int, texture):
        super().__init__(x = x , y = y , is_solid = True , breakable = False , health = 100)
        self.type = "Bedrock"
        self.texture_path = texture




BLOCK_PROPERTIES = {
    DIRT: {"is_solid": True, "breakable": True, "health": 50, "texture": "/assets/png/dirt.png"},
    STONE: {"is_solid": True, "breakable": True, "health": 200, "texture": "/assets/png/stone.png"},
    WOOD: {"is_solid": True, "breakable": True, "health": 100, "texture": "/assets/png/wood.png"},
    BEDROCK: {"is_solid": True, "breakable": False, "health": 100, "texture": "/assets/png/bedrock.png"},
}

def create_block(x: int, y: int, block_type: str) -> Block:
    props = BLOCK_PROPERTIES[block_type]
    return Block(x, y, block_type, props["is_solid"], props["breakable"], props["health"], props["texture"])













"""
Utilisation

Initialisation :
wood = WoodBlock(x : int , y : int, "/assets/png/wood.png")
stone = StoneBlock(x :  , y : int, "/assets/png/stone.png")
dirt = DirtBlock(x : int , y : int, "/assets/png/dirt.png")
bedrock = BedrockBlock(x : int , y : int, "/assets/png/bedrock.png")

Attaquer un bloc :
block.take_damage(damage : int) -> bool
Attaque le bloc. Renvoie True si le bloc est détruit, False sinon.

Afficher le bloc :
block.render() -> None
Affiche le bloc

"""