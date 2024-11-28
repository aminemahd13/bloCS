from classes.class_vivant import Vivant
from random import randint

class Zombie(Vivant):
    def __init__(self , x_spawn : int, y_spawn : int):
        super().__init__(x_spawn = x_spawn , y_spawn = y_spawn , type = "Zombie" , health = 100 , dx = 4)
        self.map = "Mine"
        self.distance_chasse = 10 * 40
    
    def act_direction(self, dict_players):
        dist2 = None
        player = None
        for all_players in dict_players.values():
            if all_players.map == self.map:
                if dist2 is None:
                    dist3 = (all_players.x_left() - self.x_left())**2 + (all_players.y_up() - self.y_up())**2
                    if dist3 <= self.distance_chasse ** 2:
                        dist2 = dist3
                        player = all_players
                else:
                    dist3 = (all_players.x_left() - self.x_left())**2 + (all_players.y_up() - self.y_up())**2
                    if dist3 < dist2:
                        dist2 = dist3
                        player = all_players
        
        if player is not None:
            if player.x_left() < self.x_left():
                if self.check_left(1) == 1:
                    self.direction = "left"
            elif player.x_left() > self.x_left():
                if self.check_right(1) == 1:
                    self.direction = "right"
            else:
                self.direction = None
            
            if self.direction == "left":
                if self.check_left(deplacement = 1) == 0:
                    self.wanna_jump = True
                else:
                    self.wanna_jump = False
            
            elif self.direction == "right":
                if self.check_right(deplacement = 1) == 0:
                    self.wanna_jump = True
                else:
                    self.wanna_jump = False
            
            else:
                if player.y_down() < self.y_down():
                    self.wanna_jump = True
                else:
                    self.wanna_jump = False
        
        else:
            self.direction = None
            self.wanna_jump = False


"""
Utilisation

zombie = Vivant(x_spawn : int , y_spawn : int)
x_spawn = indice bloc en haut de spawn
y_spawn = indice bloc en haut de spawn


zombie.render(screen , player)
Affiche le zombie sur l'écran du joueur

zombie.y_up(), zombie.y_down(), zombie.x_left(), zombie.x_right()
Coordonnées des pixels au bord du zombie

zombie.move(player)
Fait bouger le zombie et changer le skin
Prend comme argument player pour regarder sa position

zombie.take_damage(damage)
Attaque le mib. Renvoie True s'il est mort

zombie.block_near
liste de blocs aux alentours du zombie
"""