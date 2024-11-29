from classes.class_vivant import Vivant

class Zombie(Vivant):
    def __init__(self , type):
        super().__init__(type)
        self.map = "Mine"