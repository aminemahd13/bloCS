from classes.class_vivant import Vivant
from random import randint

class Zombie(Vivant):
    def __init__(self , x_spawn : int, y_spawn : int):
        super().__init__(x_spawn = x_spawn , y_spawn = y_spawn , type = "Zombie" , health = 100 , dx = 2)
    
    def move(self , player):
        #Change la diection du joueur
        self.act_direction(player)
        
        # On regarde si le joueur est en plein saut et on actualise sa data
        self.check_if_jumping()
                
        # Changement du skin
        self.change_skin()
            
        # Déplacement du perso
        self.deplacer_perso()
    
    def act_direction(self, player):
        if player.x_left() < self.x_left():
            self.direction = "left"
        elif player.x_left() > self.x_left():
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