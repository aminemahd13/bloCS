
import pygame
from classes.class_block import Block

class Tool:
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage

    def use(self, block: Block):
        return block.take_damage(self.damage)

class Pickaxe(Tool):
    def __init__(self):
        super().__init__(name="Pickaxe", damage=50)

class Sword(Tool):
    def __init__(self):
        super().__init__(name="Sword", damage=50)