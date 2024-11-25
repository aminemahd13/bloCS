from classes.class_block import DirtBlock, StoneBlock, WoodBlock, BedrockBlock, ObsidianBlock
from utils.textures import PlayerSkin

class Vivant:
    def __init__(self , type : str , x_spawn : int , y_spawn : int , health : int , dx : int):
        # [x,y] à changer en fonction du milieu de la map
        """Initializes the player
        name --> string, name of the player
        coordinates --> list of 2 integers [x,y] if coordinates = None then the player will be placed at the center of the map
        skin --> string, path to the skin of the player
        inventory --> list of items in the inventory
        health --> life points of the player
        """
        self.jump = False #Est en plein saut
        self.wanna_jump = False #Veut sauter
        self.type = type
        self.taille_block = 40
        self.x = x_spawn * self.taille_block
        self.y = y_spawn * self.taille_block
        self.direction_skin = "right"
        self.stade_animation = 1
        self.v_ini = 0
        self.V0 = 564 #Vitesse initiale lors d'un saut
        self.g = round(self.V0**2 / (2 * 2.27 * 40)) #Gravité, pour sauter d'une hauteur max de 2.3 blocs
        self.compteur_jump = 0
        self.dist_real = 0
        self.dist_theo = 0
        self.dx = dx
        self.moving = False
        self.direction = None #Horizontal , vertical
        self.block_near = []
        self.health = health
        self.dict_skins = eval(f"{type}Skin")
        self.skin = self.dict_skins["Standing Right"]
    
    def check_right(self, deplacement : int) -> int:
        """
        Renvoie le déplacement maximal pouvant être effectué sur la droite,
        inférieur à déplacement.
        """
        for block in self.block_near:
            if block.is_solid:
                if block.y_down() >= self.y_up() and block.y_up() <= self.y_down(): #Si le bloc est sur la hauteur du joueur
                    if self.x_left() < block.x_left() <= self.x_right(): #Si le bloc est dans le joueur
                        deplacement = 0
                        break
                    elif block.x_left() > self.x_right(): #Si le bloc est sur la droite
                        deplacement = min(deplacement , block.x_left() - self.x_right() - 1)
        return deplacement
    
    def check_left(self , deplacement : int) -> int:
        """
        Renvoie le déplacement maximal pouvant être effectué sur la gauche,
        inférieur à déplacement.
        """
        for block in self.block_near:
            if block.is_solid:
                if block.y_down() >= self.y_up() and block.y_up() <= self.y_down(): #Si le bloc est sur la hauteur du joueur
                    if self.x_left() <= block.x_right() < self.x_right(): #Si le bloc est dans le joueur
                        deplacement = 0
                        break
                    elif block.x_right() < self.x_left(): #Si le bloc est sur la gauche
                        deplacement = min(deplacement , self.x_left() - block.x_right() - 1)
        return deplacement
    
    def check_up(self , deplacement : int) -> int:
        """
        Renvoie le déplacement maximal pouvant être effectué vers le haut,
        inférieur à déplacement.
        """
        for block in self.block_near:
            if block.is_solid:
                if block.x_left() <= self.x_right() and block.x_right() >= self.x_left(): #Si on est aligné verticalement au joueur
                    if self.y_up() <= block.y_down() < self.y_up() + self.taille_block - 1:
                        deplacement = 0
                        break
                    elif block.y_down() < self.y_up():
                        deplacement = min(deplacement , self.y_up() - block.y_down() - 1)
        return deplacement
    
    def check_down(self , deplacement : int) -> int:
        """
        Renvoie le déplacement maximal pouvant être effectué vers le bas,
        inférieur à déplacement.
        """
        for block in self.block_near:
            if block.is_solid:
                if block.x_left() <= self.x_right() and block.x_right() >= self.x_left(): #Si on est aligné verticalement au joueur
                    if self.y_up() +self.taille_block < block.y_down() <= self.y_down():
                        deplacement = 0
                        break
                    elif block.y_up() > self.y_down():
                        deplacement = min(deplacement , block.y_up() - self.y_down() - 1)
        return deplacement
    
    def check_up_right(self , deplacement_up : int , deplacement_right : int) -> tuple:
        deplacement_up1 = self.check_up(deplacement = deplacement_up)
        deplacement_right1 = self.check_right(deplacement = deplacement_right)
        if deplacement_up1 == deplacement_up and deplacement_right1 == deplacement_right:
            for block in self.block_near:
                if block.is_solid:
                    if block.x_left() <= self.x_right() + deplacement_right and block.x_right() >= self.x_left(): #Si on est aligné verticalement au joueur
                        if block.y_down() < self.y_up():
                            deplacement_up1 = min(deplacement_up1 , self.y_up() - block.y_down() - 1)
                    if block.y_down() >= self.y_up() - deplacement_up and block.y_up() <= self.y_down(): #Si le bloc est sur la hauteur du joueur
                        if block.x_left() > self.x_right(): #Si le bloc est sur la droite
                            deplacement_right1 = min(deplacement_right1 , block.x_left() - self.x_right() - 1)
            if deplacement_up1 == deplacement_up and deplacement_right1 == deplacement_right:
                return deplacement_up1 , deplacement_right1
            elif deplacement_up1 >= deplacement_right1:
                return deplacement_up1 , deplacement_right
            else:
                return deplacement_up , deplacement_right1
        else:
            return deplacement_up1 , deplacement_right1
        
    def check_up_left(self , deplacement_up : int , deplacement_left : int) -> tuple:
        deplacement_up1 = self.check_up(deplacement = deplacement_up)
        deplacement_left1 = self.check_left(deplacement = deplacement_left)
        if deplacement_up1 == deplacement_up and deplacement_left1 == deplacement_left:
            for block in self.block_near:
                if block.is_solid:
                    if block.x_left() <= self.x_right() and block.x_right() >= self.x_left() - deplacement_left: #Si on est aligné verticalement au joueur
                        if block.y_down() < self.y_up():
                            deplacement_up1 = min(deplacement_up1 , self.y_up() - block.y_down() - 1)
                    if block.y_down() >= self.y_up() - deplacement_up and block.y_up() <= self.y_down(): #Si le bloc est sur la hauteur du joueur
                        if block.x_right() < self.x_left(): #Si le bloc est sur la droite
                            deplacement_left1 = min(deplacement_left1 , self.x_left() - block.x_right() - 1)
            if deplacement_up1 == deplacement_up and deplacement_left1 == deplacement_left:
                return deplacement_up1 , deplacement_left1
            elif deplacement_up1 >= deplacement_left1:
                return deplacement_up1 , deplacement_left
            else:
                return deplacement_up , deplacement_left1
        else:
            return deplacement_up1 , deplacement_left1
    
    def check_down_right(self , deplacement_down : int , deplacement_right : int) -> tuple:
        deplacement_down1 = self.check_down(deplacement = deplacement_down)
        deplacement_right1 = self.check_right(deplacement = deplacement_right)
        if deplacement_down1 == deplacement_down and deplacement_right1 == deplacement_right:
            for block in self.block_near:
                if block.is_solid:
                    if block.x_left() <= self.x_right() + deplacement_right and block.x_right() >= self.x_left(): #Si on est aligné verticalement au joueur
                        if block.y_up() > self.y_down():
                            deplacement_down1 = min(deplacement_down1 , block.y_up() - self.y_down() - 1)
                    if block.y_down() >= self.y_up() and block.y_up() <= self.y_down() + deplacement_down: #Si le bloc est sur la hauteur du joueur
                        if block.x_left() > self.x_right(): #Si le bloc est sur la droite
                            deplacement_right1 = min(deplacement_right1 , block.x_left() - self.x_right() - 1)
            if deplacement_down1 == deplacement_down and deplacement_right1 == deplacement_right:
                return deplacement_down1 , deplacement_right1
            elif deplacement_down1 >= deplacement_right1:
                return deplacement_down1 , deplacement_right
            else:
                return deplacement_down , deplacement_right1
        else:
            return deplacement_down1 , deplacement_right1
    
    def check_down_left(self , deplacement_down : int , deplacement_left : int) -> tuple:
        deplacement_down1 = self.check_down(deplacement = deplacement_down)
        deplacement_left1 = self.check_left(deplacement = deplacement_left)
        if deplacement_down1 == deplacement_down and deplacement_left1 == deplacement_left:
            for block in self.block_near:
                if block.is_solid:
                    if block.x_left() <= self.x_right() and block.x_right() >= self.x_left() - deplacement_left: #Si on est aligné verticalement au joueur
                        if block.y_up() > self.y_down():
                            deplacement_down1 = min(deplacement_down1 , block.y_up() - self.y_down() - 1)
                    if block.y_down() >= self.y_up() and block.y_up() <= self.y_down() + deplacement_down: #Si le bloc est sur la hauteur du joueur
                        if block.x_right() < self.x_left(): #Si le bloc est sur la droite
                            deplacement_left1 = min(deplacement_left1 , self.x_left() - block.x_right() - 1)
            if deplacement_down1 == deplacement_down and deplacement_left1 == deplacement_left:
                return deplacement_down1 , deplacement_left1
            elif deplacement_down1 >= deplacement_left1:
                return deplacement_down1 , deplacement_left
            else:
                return deplacement_down , deplacement_left1
        else:
            return deplacement_down1 , deplacement_left1
    
    def check_if_jumping(self):
        reinitialisation_saut = False #Variable servant à réinitialiser les variables de saut
    
        if not self.jump: #Si le joueur n'est pas en plein saut
            #On vérifie qu'il y a bien qqlq chose en dessous de lui, sinon il chute
            if self.check_down(deplacement = 1) == 1:
                self.jump = True #Le joueur chute
                #On initialise les paramètres de chute à 0
                self.v_ini = 0 #Vitesse initiale de la chute
                reinitialisation_saut = True
            
            #S'il y a un bloc sous ses pieds, on regarde si le joueur veut sauter
            elif self.wanna_jump:
                if self.check_up(deplacement = 1) == 1:
                    self.jump = True #Le joueur saute
                    self.v_ini = self.V0 #La vitesse initiale cette fois vaut V0
                    reinitialisation_saut = True
        
        
        else: #Si le joueur est déjà en plein saut
            if self.direction == "right":
                #Si le joueur veut aller à droite
                #Soit il appuie à droite et pas à gauche, soit il appuyait pas à droite la frame d'avant mais maintenant oui
                if self.check_down_right(deplacement_down = 1 , deplacement_right = 1)[0] == 0:
                    #S'il y a quelque chose sous ses pieds, dès qu'il veut aller en bas à droite, le joueur arrête sa chute
                    self.jump = False
                    self.v_ini = 0
                    reinitialisation_saut = True
            elif self.direction == "left":
                #Si le joueur veut aller à gauche
                #Soit il appuie à gauche et pas à droite, soit il appuyait pas à gauche la frame d'avant mais maintenant oui
                if self.check_down_left(deplacement_down = 1 , deplacement_left = 1)[0] == 0:
                    #S'il y a quelque chose sous ses pieds, dès qu'il veut aller en bas à gauche, le joueur arrête sa chute
                    self.jump = False
                    self.v_ini = 0
                    reinitialisation_saut = True
            else:
                #S'il n'y a pas de direction particulière (gauche ou droite)
                if self.check_down(deplacement = 1) == 0:
                    #S'il y a qqlq chose en dessous de lui, la chute s'arrête
                    self.jump = False
                    self.v_ini = 0
                    reinitialisation_saut = True
            if self.check_up(deplacement = 2) <= 1:
                #S'il y a un bloc au dessus de lui, la chute ne s'arrête pas mais la vitesse se réinitialise
                self.v_ini = 0
                reinitialisation_saut = True

        if reinitialisation_saut:
            self.compteur_jump = 0
            self.dist_real = 0
            self.dist_theo = 0

    def deplacer_perso(self):
        deplacement_down , deplacement_up , deplacement_right , deplacement_left = None , None , None , None
        if self.jump: #Si le joueur est en plein saut
            #On calcule la nouvelle distance théorique
            self.compteur_jump += 1
            self.dist_theo = (self.v_ini - self.g * self.compteur_jump // 120) * self.compteur_jump // 60
            #Déplacement à effectuer
            depl = self.dist_theo - self.dist_real
            self.dist_real = self.dist_theo #On actualise la vraie distance
            #Remarque : s'il y a un mur en haut ou en bas, le personnage n vas pas bouger verticalement de depl
            #Cependant, à la frame d'après, le jeu va détecter s'il est contre ce mur, et la chute va stopper
            if depl > 0: #Si on monte
                if self.direction == "right":
                    #Si on va à droite
                    #On calcule les déplacements qu'on va effectivement réaliser dans les deux directions
                    deplacement_up , deplacement_right = self.check_up_right(deplacement_up = depl , deplacement_right = self.dx)
                elif self.direction == "left":
                    #Si on va à gauche
                    #On calcule les déplacements qu'on va effectivement réaliser dans les deux directions
                    deplacement_up , deplacement_left = self.check_up_left(deplacement_up = depl , deplacement_left = self.dx)
                else:
                    #Si on ne bouge pas horizontalement, on monte simplement
                    deplacement_up = self.check_up(deplacement = depl)
            
            elif depl < 0: #Si on descend
                if self.direction == "right":
                    #Si on va à droite
                    #On calcule les déplacements qu'on va effectivement réaliser dans les deux directions
                    deplacement_down , deplacement_right = self.check_down_right(deplacement_down = -depl , deplacement_right = self.dx)
                elif self.direction == "left":
                    #Si on va à gauche
                    #On calcule les déplacements qu'on va effectivement réaliser dans les deux directions
                    deplacement_down , deplacement_left = self.check_down_left(deplacement_down = -depl , deplacement_left = self.dx)
                else:
                    #Si on ne bouge pas horizontalement, on monte simplement
                    deplacement_down = self.check_down(deplacement = -depl)
                    
            else: #Si on ne bouge pas verticalement
                if self.direction == "right":
                    #Si on va à droite
                    #On calcule le déplacement qu'on va effectivement réaliser dans la direction
                    deplacement_right = self.check_right(deplacement = self.dx)
                elif self.direction == "left":
                    #Si on va à gauche
                    #On calcule le déplacement qu'on va effectivement réaliser dans la direction
                    deplacement_left = self.check_left(deplacement = self.dx)


        else: #Si on est pas en plein saut
            if self.direction == "right":
                #Si on va à droite
                #On calcule le déplacement qu'on va effectivement réaliser dans la direction
                deplacement_right = self.check_right(deplacement = self.dx)
            if self.direction == "left":
                #Si on va à gauche
                #On calcule le déplacement qu'on va effectivement réaliser dans la direction
                deplacement_left = self.check_left(deplacement = self.dx)

        
        
        
        #On effectue les éventuels déplacements
        
        if deplacement_down is not None:
            self.y += deplacement_down
        if deplacement_up is not None:
            self.y -= deplacement_up
        if deplacement_left is not None:
            self.x -= deplacement_left
        if deplacement_right is not None:
            self.x += deplacement_right
         
    def move(self):
        #Change la diection du joueur
        self.act_direction()
        
        # On regarde si le joueur est en plein saut et on actualise sa data
        self.check_if_jumping()
                
        # Changement du skin
        self.change_skin()
            
        # Déplacement du perso
        self.deplacer_perso()
    
    def take_damage(self , damage):
        self.health -= damage
        if self.health <= 0:
            return True
        return False
       
    def change_skin(self):
        """
        Change le skin.
        """
        self.moving = False
        if self.direction is not None:
            self.direction_skin = self.direction
            self.moving = True
        else:
            self.moving = False
        
        #Jumping
        if self.jump:
            if self.direction_skin == "right":
                self.skin = self.dict_skins["Jumping Right"]
                 
            elif self.direction_skin == "left":
                self.skin = self.dict_skins["Jumping Left"]
            
        #Not jumping
        else:
            #Changing stade --> moving right or left if he was in opposite direction
            if self.moving:
                if self.stade_animation == 20:
                    self.stade_animation = 1
                else:
                    self.stade_animation += 1

                
            #Moving right
            if self.direction_skin == "right":
                if self.stade_animation <= 10:
                    self.skin = self.dict_skins["Walking Right"]
                else :
                    self.skin = self.dict_skins["Standing Right"]
                        
                
            #Moving left  
            elif self.direction_skin == "left":
                if self.stade_animation <= 10:
                    self.skin = self.dict_skins["Walking Left"]
                else :
                    self.skin = self.dict_skins["Standing Left"]
    
    def y_up(self):
        """
        Coordonnée y en haut.
        """
        return self.y
    
    def y_down(self):
        """
        Coordonnée y en bas.
        """
        return self.y + 2 * self.taille_block - 1
    
    def x_left(self):
        """
        Coordonnée x à gauche.
        """
        return self.x
    
    def x_right(self):
        """
        Coordonnée x à droite.
        """
        return self.x + self.taille_block - 1
    
    def render(self , screen , player):
        """
        Affiche le mob sur l'écran.
        """
        x_screen = self.x - player.x_left() + player.get_x_screen()
        y_screen = self.y - player.y_left() + player.get_y_screen()
        screen.blit(self.skin, (x_screen, y_screen))

    

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