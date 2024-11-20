import pygame
from utils.coord_to_screen import screen_to_coord, coord_to_indice
from classes.class_block import Block, DirtBlock, StoneBlock, WoodBlock, BedrockBlock, ObsidianBlock
import utils.key_handler as key

######### inventory est un dictionnaire avec les items en clé et le nombre d'items en valeur #########



class Player:
    def __init__(self , height_screen : int , width_screen : int , x_spawn : int = 33 , y_spawn : int = 6, name : str = "Player 1"):
        # [x,y] à changer en fonction du milieu de la map
        """Initializes the player
        name --> string, name of the player
        coordinates --> list of 2 integers [x,y] if coordinates = None then the player will be placed at the center of the map
        skin --> string, path to the skin of the player
        inventory --> list of items in the inventory
        health --> life points of the player
        """
        self.jump = False
        self.name = name
        self.mining = False
        self.taille_block = 40
        self.x_screen = height_screen // 2 - self.taille_block // 2
        self.y_screen = width_screen // 2 - self.taille_block
        self.width_screen = width_screen
        self.height_screen = height_screen
        self.x = x_spawn * self.taille_block
        self.y = y_spawn * self.taille_block
        self.direction = "right"
        self.stade = 1
        self.v_ini=0
        self.V0 = 551 #Vitesse initiale lors d'un saut
        self.g = round(self.V0**2 / (2 * 2.3 * 40)) #Gravité, pour sauter d'une hauteur max de 2.3 blocs
        self.compteur_jump = 0
        self.dist_real = 0
        self.dist_theo = 0
        self.dx = 6
        self.moving = False
        self.key_right = key.right()
        self.key_left = key.left()
        self.key_up = key.up()
        self.hist_touches = {"right" : key.right() , "left" : key.left()}
        self.block_near = []
        self.selected_block = 1
        self.block_types = ["Dirt", "Stone", "Obsidian", "Wood", "Bedrock"]
        # Define a custom event for resetting the mining state
        self.RESET_MINING_EVENT = pygame.USEREVENT + 1
        
        self.inventory = {
            "Dirt" : 10,
            "Stone" : 10,
            "Obsidian" : 10,
            "Wood" : 10,
            "Bedrock" : 10,
        }
        self.health = 100
        self.skin_path = "assets/graphics/standing_right.png"
        self.skin = pygame.image.load(self.skin_path)
    
    
    def act_hist_touches(self):
        self.hist_touches["right"] = self.key_right
        self.hist_touches["left"] = self.key_left
    
    def act_touches(self):
        self.key_right = key.right()
        self.key_left = key.left()
        self.key_up = key.up()
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
        self.moving = False
        if (self.key_right and not self.key_left) or (not self.hist_touches["right"] and self.key_right):
            #Si le joueur veut aller à droite
            #Soit il appuie à droite et pas à gauche, soit il appuyait pas à droite la frame d'avant mais maintenant oui
            self.direction = "right" #On force la direction du skin
            self.moving = True #On indique que le skin est en mouvement
        elif (self.key_left and not self.key_right) or ((not self.hist_touches["left"] and self.key_left)):
            #Si le joueur veut aller à gauche
            #Soit il appuie à gauche et pas à droite, soit il appuyait pas à gauche la frame d'avant mais maintenant oui
            self.direction = "left" #On force la direction du skin
            self.moving = True #On indique que le skin est en mouvement
        else:
            #Pas de direction imposée : on n'impose pas le skin
            self.moving = False #On ne fait pas l'animation de marche
        
        
        #Not mining
        if not self.mining:
            #Jumping
            if self.jump:
                if self.direction == "right":
                    self.skin_path = "assets/graphics/jumping_right.png"
                    self.skin = pygame.image.load(self.skin_path)
                    
                elif self.direction == "left":
                    self.skin_path = "assets/graphics/jumping_left.png"
                    self.skin = pygame.image.load(self.skin_path)
            
            #Not jumping
            else:
                #Changing stade --> moving right or left if he was in opposite direction
                if self.moving:
                    if self.stade == 20:
                        self.stade = 1
                    else:
                        self.stade += 1

                
                #Moving right
                if self.direction == "right":
                    if self.stade <= 20//2:
                        self.skin_path = "assets/graphics/walking_right.png"
                        self.skin = pygame.image.load(self.skin_path)
                    else :
                        self.skin_path = "assets/graphics/standing_right.png"
                        self.skin = pygame.image.load(self.skin_path)
                        
                
                #Moving left  
                elif self.direction == "left":
                    if self.stade <= 20//2:
                        self.skin_path = "assets/graphics/walking_left.png"
                        self.skin = pygame.image.load(self.skin_path)
                    else :
                        self.skin_path = "assets/graphics/standing_left.png"
                        self.skin = pygame.image.load(self.skin_path)  
                        
            
        
        #Mining
        else:
            if self.direction == "right":
                self.skin_path = "assets/graphics/mining_right.png"
                self.skin = pygame.image.load(self.skin_path)
                
            elif self.direction == "left":
                self.skin_path = "assets/graphics/mining_left.png"
                self.skin = pygame.image.load(self.skin_path)
        
        self.skin = pygame.transform.scale(self.skin, (40, 80))
                
    
    def check_if_jumping(self , background):
        reinitialisation_saut = False #Variable servant à réinitialiser les variables de saut
    
        if not self.jump: #Si le joueur n'est pas en plein saut
            #On vérifie qu'il y a bien qqlq chose en dessous de lui, sinon il chute
            if background.check_down(player = self,
                                    deplacement = 1 #On regarde le déplacement possible pour un déplacement "élémentaire"
                                    ) == 1:
                self.jump = True #Le joueur chute
                #On initialise les paramètres de chute à 0
                self.v_ini = 0 #Vitesse initiale de la chute
                reinitialisation_saut = True
            
            #S'il y a un bloc sous ses pieds, on regarde si le joueur veut sauter
            elif self.key_up:
                if background.check_up(player = self,
                                        deplacement = 1 #On regarde le déplacement possible pour un déplacement "élémentaire"
                                        ) == 1:
                    self.jump = True #Le joueur saute
                    self.v_ini = self.V0 #La vitesse initiale cette fois vaut V0
                    reinitialisation_saut = True
        
        
        else: #Si le joueur est déjà en plein saut
            if (self.key_right and not self.key_left) or (not self.hist_touches["right"] and self.key_right):
                #Si le joueur veut aller à droite
                #Soit il appuie à droite et pas à gauche, soit il appuyait pas à droite la frame d'avant mais maintenant oui
                if background.check_down_right(player = self,
                                            deplacement_down = 1, #On regarde le déplacement possible pour un déplacement "élémentaire"
                                            deplacement_right = 1
                                            )[0] == 0:
                    #S'il y a quelque chose sous ses pieds, dès qu'il veut aller en bas à droite, le joueur arrête sa chute
                    self.jump = False
                    self.v_ini = 0
                    reinitialisation_saut = True
            elif (self.key_left and not self.key_right) or (not self.hist_touches["left"] and self.key_left):
                #Si le joueur veut aller à gauche
                #Soit il appuie à gauche et pas à droite, soit il appuyait pas à gauche la frame d'avant mais maintenant oui
                if background.check_down_left(player = self,
                                            deplacement_down = 1, #On regarde le déplacement possible pour un déplacement "élémentaire"
                                            deplacement_left = 1
                                            )[0] == 0:
                    #S'il y a quelque chose sous ses pieds, dès qu'il veut aller en bas à gauche, le joueur arrête sa chute
                    self.jump = False
                    self.v_ini = 0
                    reinitialisation_saut = True
            else:
                #S'il n'y a pas de direction particulière (gauche ou droite)
                if background.check_down(player = self,
                                        deplacement = 1 #On regarde le déplacement possible pour un déplacement "élémentaire"
                                        ) == 0:
                    #S'il y a qqlq chose en dessous de lui, la chute s'arrête
                    self.jump = False
                    self.v_ini = 0
                    reinitialisation_saut = True
            if background.check_up(player = self,
                                deplacement = 2 #On regarde le déplacement possible pour un déplacement "élémentaire"
                                ) <= 1:
                #S'il y a un bloc au dessus de lui, la chute ne s'arrête pas mais la vitesse se réinitialise
                self.v_ini = 0
                reinitialisation_saut = True

        if reinitialisation_saut:
            self.compteur_jump = 0
            self.dist_real = 0
            self.dist_theo = 0
    
    
    
    def deplacer_perso(self , background):
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
                if (self.key_right and not self.key_left) or (not self.hist_touches["right"] and self.key_right):
                    #Si on va à droite
                    #On calcule les déplacements qu'on va effectivement réaliser dans les deux directions
                    deplacement_up , deplacement_right = background.check_up_right(player = self,
                                                                                deplacement_up = depl,
                                                                                deplacement_right = self.dx)
                elif (self.key_left and not self.key_right) or ((not self.hist_touches["left"] and self.key_left)):
                    #Si on va à gauche
                    #On calcule les déplacements qu'on va effectivement réaliser dans les deux directions
                    deplacement_up , deplacement_left = background.check_up_left(player = self,
                                                                                deplacement_up = depl,
                                                                                deplacement_left = self.dx)
                else:
                    #Si on ne bouge pas horizontalement, on monte simplement
                    deplacement_up = background.check_up(player = self,
                                                        deplacement = depl)
            
            elif depl < 0: #Si on descend
                if (self.key_right and not self.key_left) or (not self.hist_touches["right"] and self.key_right):
                    #Si on va à droite
                    #On calcule les déplacements qu'on va effectivement réaliser dans les deux directions
                    deplacement_down , deplacement_right = background.check_down_right(player = self,
                                                                                    deplacement_down = -depl,
                                                                                    deplacement_right = self.dx)
                elif (self.key_left and not self.key_right) or ((not self.hist_touches["left"] and self.key_left)):
                    #Si on va à gauche
                    #On calcule les déplacements qu'on va effectivement réaliser dans les deux directions
                    deplacement_down , deplacement_left = background.check_down_left(player = self,
                                                                                    deplacement_down = -depl,
                                                                                    deplacement_left = self.dx)
                else:
                    #Si on ne bouge pas horizontalement, on monte simplement
                    deplacement_down = background.check_down(player = self,
                                                            deplacement = -depl)
                    
            else: #Si on ne bouge pas verticalement
                if (self.key_right and not self.key_left) or (not self.hist_touches["right"] and self.key_right):
                    #Si on va à droite
                    #On calcule le déplacement qu'on va effectivement réaliser dans la direction
                    deplacement_right = background.check_right(player = self,
                                                            deplacement = self.dx)
                elif (self.key_left and not self.key_right) or (not self.hist_touches["left"] and self.key_left):
                    #Si on va à gauche
                    #On calcule le déplacement qu'on va effectivement réaliser dans la direction
                    deplacement_left=background.check_left(player = self,
                                                        deplacement = self.dx)


        else: #Si on est pas en plein saut
            if (self.key_right and not self.key_left) or (not self.hist_touches["right"] and self.key_right):
                #Si on va à droite
                #On calcule le déplacement qu'on va effectivement réaliser dans la direction
                deplacement_right = background.check_right(player = self,
                                                        deplacement = self.dx)
            if (self.key_left and not self.key_right) or (not self.hist_touches["left"] and self.key_left):
                #Si on va à gauche
                #On calcule le déplacement qu'on va effectivement réaliser dans la direction
                deplacement_left = background.check_left(player = self,
                                                        deplacement = self.dx)

        
        
        
        #On effectue les éventuels déplacements
        
        if deplacement_down is not None:
            self.y += deplacement_down
        if deplacement_up is not None:
            self.y -= deplacement_up
        if deplacement_left is not None:
            self.x -= deplacement_left
        if deplacement_right is not None:
            self.x += deplacement_right
    
    
    
    def mining_or_breaking(self , background , event):
        x_screen, y_screen = pygame.mouse.get_pos() #Position du click sur l'écran
        #On converti ces coordonnées en coordonnées relatives au background (en px)
        x , y = screen_to_coord(x_screen = x_screen , y_screen = y_screen , player = self)
        if self.x_left() - 80 <= x <= self.x_right() + 80 and self.y_up() - 80 <= y <= self.y_down() + 80:
            #Si on est dans une fenêtre de 2 blocs sur les côtés
            if event.button == 1 and not (self.x_left()<=x<=self.x_right() and self.y_up()<=y<=self.y_down()):  # Left click to place a block
                x_indice , y_indice = coord_to_indice(x = x , y = y)
                if x_indice*40+40-1<self.x_left() or x_indice*40>self.x_right() or y_indice*40>self.y_down() or y_indice*40+40-1<self.y_up():
                    selected_block_type = self.block_types[self.selected_block - 1] #Type de bloc sélectionné
                    if self.inventory[selected_block_type] > 0: #Si on en a dans notre inventaire
                        new_block = eval(f"{selected_block_type}Block(x_indice = x_indice , y_indice = y_indice)") #Création de l'objet block
                        if background.add_block(new_block): #Si le bloc a été placé
                            self.remove_inventory(selected_block_type) #On l'enlève de l'inventaire
            elif event.button == 3:  # Right click to remove a block
                background.damage_block(x = x, y = y, damage = 100, player = self) # Remove 100 hp from the block
                #Remarque : met automatiquement le bloc dans l'inventaire du joueur s'il est détruit
                self.mining = True
                pygame.time.set_timer(self.RESET_MINING_EVENT, 350)  # Set a timer for 1 second
    
    
    
    def draw_inventory(self , screen):
        font = pygame.font.Font(None, int(36 * screen.get_height() / 1080))
        block_images = {
            "Dirt": pygame.image.load("assets/graphics/dirt.png"),
            "Stone": pygame.image.load("assets/graphics/stone.png"),
            "Obsidian": pygame.image.load("assets/graphics/obsidian.png"),
            "Wood": pygame.image.load("assets/graphics/dirt.png"),
            "Bedrock": pygame.image.load("assets/graphics/bedrock.png")
        }
        x_offset = 10
        y_offset = 10
        for i, block_type in enumerate(self.block_types):
            block_image = pygame.transform.scale(block_images[block_type], (int(40 * screen.get_height() / 1080), int(40 * screen.get_height() / 1080)))
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
    
    
    def render(self , screen):
        if self.skin:
            screen.blit(self.skin, (self.x_screen, self.y_screen))
            
    
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
            
        
"""

#####################Exemple d'utilisation#####################
player=Player(height_screen = 1920 , width_screen = 1080 , name = "Player 1")
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

        
        

        
        
        
        
        