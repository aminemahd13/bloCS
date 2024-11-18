


class Block:
    def __init__(self, x : int , y : int , is_solid : bool = True, breakable : bool = True , health : int = 100):
        """
        Initialize a block.
        :param position: A tuple (x, y) representing the block's position.
        :param is_solid: Whether the block can be passed through.
        :param breakable: Whether the block can be broken.
        :param health: The starting health of the block.
        """
        self.x = x
        self.y = y
        self.is_solid = is_solid
        self.breakable = breakable
        self.health = health

    def take_damage(self, amount : int) -> None:
        """
        Reduces the block's health.
        :param amount: The amount of damage to apply.
        """
        if self.breakable:
            self.health -= amount
            if self.health <= 0:
                self.break_block()
        else:
            print(f"This block is unbreakable!")

    def break_block(self):
        """
        Handles block destruction.
        """
        print(f"The block at {(self.x , self.y)} is destroyed!")
        # Remove block logic here

    def render(self):
        """
        Renders the block.
        """
        print(f"Rendering block at {(self.x , self.y)}")




class DirtBlock(Block):
    def __init__(self, position):
        super().__init__(position, is_solid=True, breakable=True, health=50)

    def render(self):
        print(f"Rendering block at {self.position}")



class StoneBlock(Block):
    def __init__(self, position):
        super().__init__(position, is_solid=True, breakable=True, health=200)

    def render(self):
        print(f"Rendering block at {self.position}")



class WoodBlock(Block):
    def __init__(self, position):
        super().__init__(position, is_solid=True, breakable=True, health=100)

    def render(self):
        print(f"Rendering block at {self.position}")


class BedRock(Block):
    def __init__(self, position):
        super().__init__(position, is_solid=True, breakable=False, health=100)

    def render(self):
        print(f"Rendering block at {self.position}")