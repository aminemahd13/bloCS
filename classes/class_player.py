import pygame
from utils.coord_to_screen import screen_to_coord, coord_to_indice
from classes.class_block import Block, DirtBlock, StoneBlock, WoodBlock, BedrockBlock, ObsidianBlock
import utils.key_handler as key
from game.main import jeu , spawn_new_tile
from random import randint
from utils.textures import block_images, PlayerSkin



class Vivant:
    def __init__(self , type : str , x_spawn : int , y_spawn : int):
        # [x,y] à changer en fonction du milieu de la map
        """Initializes the player
        name --> string, name of the player
        coordinates --> list of 2 integers [x,y] if coordinates = None then the player will be placed at the center of the map
        skin --> string, path to the skin of the player
        inventory --> list of items in the inventory
        health --> life points of the player
        """
        self.jump = False
        self.wanna_jump = False
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
        self.dx = 0
        self.moving = False
        self.direction = [None , None] #Horizontal , vertical
        self.block_near = []
        self.health = 0
        self.dict_skins = eval(f"{type}Skin")
        self.skin = self.dict_skins["Standing Right"]
    
    def change_skin(self):
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
    
    
    def render(self , screen , player):
        x_screen = self.x - player.x + player.x_screen
        y_screen = self.y - player.y + player.y_screen
        screen.blit(self.skin, (x_screen, y_screen))
    
    def act_direction(self):
        pass #Définir un truc pour actualiser la direction des mobs


class Player(Vivant):
    def __init__(self , height_screen : int , width_screen : int , x_spawn : int = 33 , y_spawn : int = 6, name : str = "Player 1"):
        # [x,y] à changer en fonction du milieu de la map
        """Initializes the player
        name --> string, name of the player
        coordinates --> list of 2 integers [x,y] if coordinates = None then the player will be placed at the center of the map
        skin --> string, path to the skin of the player
        inventory --> list of items in the inventory
        health --> life points of the player
        """
        super().__init__(x_spawn = x_spawn , y_spawn = y_spawn , type = "Player")
        self.dx = 5
        self.health = 100
        self.name = name
        self.height_screen = height_screen
        self.width_screen = width_screen
        self.x_screen = height_screen // 2 - self.taille_block // 2
        self.y_screen = width_screen // 2 - self.taille_block
        self.is_playing_2048 = False
        self.changed = False
        self.grille = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        self.mining = False
        self.key_close = key.close()
        self.hist_touches = {"right" : key.right() , "left" : key.left() , "echap" : key.close()}
        self.selected_block = 1
        self.block_types = ["Dirt", "Stone", "Obsidian", "Bedrock"]
        # Define a custom event for resetting the mining state
        self.RESET_MINING_EVENT = pygame.USEREVENT + 1
        
        self.inventory = {
            "Dirt" : 10,
            "Stone" : 0,
            "Obsidian" : 0,
            "Bedrock" : 0
        }
        self.inventory_tuiles = {
            "2" : 0,
            "4" : 0,
            "8" : 0,
            "16" : 0,
            "32" : 0,
            "64" : 0,
            "128" : 0,
            "256" : 0,
            "512" : 0,
            "1024" : 0,
            "2048" : 0
        }
    
    def render(self , screen):
        screen.blit(self.skin, (self.x_screen, self.y_screen))
    
    def act_direction(self):
        if key.right() and (not self.hist_touches["right"] or not key.left()):
            self.direction = "right"
        elif key.left() and (not self.hist_touches["left"] or not key.right()):
            self.direction = "left"
        else:
            self.direction = None
        
        self.wanna_jump = key.up()
    
    
    def tuile_max(self):
        m = 0
        for ligne in self.grille:
            for tuile in ligne:
                m = max(m , tuile)
        return m
    
    def change_map(self , background):
        if 38 * 40 <= self.x_left() and self.x_right() <= 40 * 40 and 6 * 40 == self.y_up():
            if not self.changed:
                    background.change_mod()
                    self.changed = True
        else:
            self.changed = False
    
    
    def act_hist_touches(self):
        self.hist_touches["close"] = key.close()
        self.hist_touches["right"] = key.right()
        self.hist_touches["left"] = key.left()
        self.hist_touches["up"] = key.up()
        key_get_number = key.get_number()
        if key_get_number != -1: #Si on clique sur un chiffre correct pour sélectionner un bloc
            self.selected_block = int(key_get_number) #On change la sélection        

    
    def change_skin(self) -> None:
        
        """Player Movement
        keyboard_jump --> True or False if jump
        keyboard_direction --> string, direction of the player
        mining --> True or False if mining
        we change skin depending on the direction or if he jump or mining
        """
        #Not mining
        if not self.mining:                        
            super().change_skin()
        
        #Mining
        else:
            self.moving = False
            if self.direction is not None:
                self.direction_skin = self.direction
                self.moving = True
            else:
                self.moving = False
            tuile_max = self.tuile_max()
            if self.direction_skin == "right":
                if tuile_max in [0 , 2 , 4 , 8]:
                    self.skin = self.dict_skins["Mining Right"]
                elif tuile_max in [16 , 32]:
                    self.skin = self.dict_skins["Mining Right Grey"]
                elif tuile_max in [64 , 128]:
                    self.skin = self.dict_skins["Mining Right Gold"]
                else:
                    self.skin = self.dict_skins["Mining Right Purple"]
                
            elif self.direction_skin == "left":
                if tuile_max in [0 , 2 , 4 , 8]:
                    self.skin = self.dict_skins["Mining Left"]
                elif tuile_max in [16 , 32]:
                    self.skin = self.dict_skins["Mining Left Grey"]
                elif tuile_max in [64 , 128]:
                    self.skin = self.dict_skins["Mining Left Gold"]
                else:
                    self.skin = self.dict_skins["Mining Left Purple"]
                
    
    
    def mining_or_breaking(self , background , event):
        x_screen, y_screen = pygame.mouse.get_pos() #Position du click sur l'écran
        #On converti ces coordonnées en coordonnées relatives au background (en px)
        x , y = screen_to_coord(x_screen = x_screen , y_screen = y_screen , player = self)
        x_indice , y_indice = coord_to_indice(x = x , y = y)
        if self.x_left() - 80 <= x <= self.x_right() + 80 and self.y_up() - 80 <= y <= self.y_down() + 80:
            #Si on est dans une fenêtre de 2 blocs sur les côtés
            if event.button == 1 and not (self.x_left()<=x<=self.x_right() and self.y_up()<=y<=self.y_down()):  # Left click to place a block
                if x_indice*40+40-1<self.x_left() or x_indice*40>self.x_right() or y_indice*40>self.y_down() or y_indice*40+40-1<self.y_up():
                    selected_block_type = self.block_types[self.selected_block - 1] #Type de bloc sélectionné
                    if self.inventory[selected_block_type] > 0: #Si on en a dans notre inventaire
                        new_block = eval(f"{selected_block_type}Block(x_indice = x_indice , y_indice = y_indice)") #Création de l'objet block
                        if background.add_block(new_block): #Si le bloc a été placé
                                self.remove_inventory(selected_block_type) #On l'enlève de l'inventaire
            elif event.button == 3:  # Right click to remove a block
                added = False
                for key , values in background.dict_block.items():
                    for i , block in enumerate(values):
                        if block.x_indice == x_indice and block.y_indice == y_indice:
                            if block.type != "Game":
                                if block.take_damage(damage = 100 , tuile_max = self.tuile_max()):
                                    values.pop(i)
                                    if block.type == "Tuile":
                                        self.inventory_tuiles[str(block.value)] += 1
                                    else:
                                        self.add_inventory(key)
                                added=True
                                #Remarque : met automatiquement le bloc dans l'inventaire du joueur s'il est détruit
                                self.mining = True
                                pygame.time.set_timer(self.RESET_MINING_EVENT, 350)  # Set a timer for 1 second
                                break
                            else:
                                self.is_playing_2048 = True
                                added=True
                                break
                    if added:
                        break
                    
                    
    def play_2048(self , screen):
        if self.is_playing_2048:
            keys = []
            for key in self.inventory_tuiles.keys():
                if self.inventory_tuiles[key]>0:
                    keys.append([int(key),self.inventory_tuiles[key]])
            add = True
            while add and len(keys)>0:
                r = randint(0, len(keys) - 1)
                value = keys[r][0]
                add = spawn_new_tile(grid = self.grille , value = value)
                if add:
                    keys[r][1] -= 1
                    self.inventory_tuiles[str(keys[r][0])] -= 1
                    if keys[r][1] == 0:
                        keys.pop(r)
            self.is_playing_2048 = jeu(self.grille , screen , self.hist_touches)
    
    
    def draw_inventory(self , screen):
        font = pygame.font.Font(None, int(36 * screen.get_height() / 1080))
        x_offset = 10
        y_offset = 10
        for i, block_type in enumerate(self.block_types):
            block_image = block_images[block_type]
            if i+1 == self.selected_block:
                pygame.draw.rect(screen, (0, 255, 0), (x_offset + i * int(90 * screen.get_height() / 1080) - 5, y_offset - 5, int(50 * screen.get_height() / 1080), int(50 * screen.get_height() / 1080)), 3)
            screen.blit(block_image, (x_offset + i * int(90 * screen.get_height() / 1080), y_offset))
            n = self.inventory[block_type]
            text = font.render(str(n), True, (0, 0, 0))
            screen.blit(text, (x_offset + i * int(90 * screen.get_height() / 1080) + int(45 * screen.get_height() / 1080), y_offset + int(10 * screen.get_height() / 1080)))
    
    
    def add_inventory(self,item) -> None:
        """Add item to the inventory"""
        self.inventory[item] += 1
       
        
    def remove_inventory(self,item) -> None:
        """Remove item to the inventory"""
        self.inventory[item] -= 1



class Zombie(Vivant):
    def __init__(self , x_spawn : int, y_spawn : int):
        super().__init__(x_spawn = x_spawn , y_spawn = y_spawn , type = "Zombie")
        self.dx = 2 #Vitesse de déplacement
        self.health = 100
    
    
    
"""

#####################Exemple d'utilisation#####################
self=Player(height_screen = 1920 , width_screen = 1080 , name = "self 1")
print(player.name)
print(player.x)
print(player.y)
print(player.inventory)
print(player.health)
print(player.skin)

#Change skin première fois
player.change_skin(keyboard_direction = "right" , mining = False)
print(player.skin_path)
#Change skin deuxième fois --> animation
player.change_skin(keyboard_direction = "right" , mining = False)
print(player.skin_path)
#Change skin mining 
player.change_skin(keyboard_direction = "right" , mining = True)
print(player.skin_path)


"""








