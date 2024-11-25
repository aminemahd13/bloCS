from classes.class_vivant import Vivant
from random import randint

class Zombie(Vivant):
    def __init__(self , x_spawn : int, y_spawn : int):
        super().__init__(x_spawn = x_spawn , y_spawn = y_spawn , type = "Zombie" , health = 100 , dx = 2)
    
    def act_direction(self):
        pass #Définir un truc pour actualiser la direction des mobs
        #self.direction = "right" or "left"
        #self.wanna_jump = True ou False



"""
Utilisation

mob = Vivant(type : str , x_spawn : int , y_spawn : int , health : int , dx : int)
type : "Zombie","Player",...
x_spawn = indice bloc en haut de spawn
y_spawn = indice bloc en haut de spawn
health = vie
dx = déplacement sur les cotés


mob.render(screen , player)
Affiche le mob sur l'écran du joueur

mob.y_up(), mob.y_down(), mob.x_left(), mob.x_right()
Coordonnées des pixels au bord du mob

mob.move()
Fait bouger le mob et changer le skin

mob.take_damage(damage)
Attaque le mib. Renvoie True s'il est mort

mob.block_near
liste de blocs aux alentours du mob
"""