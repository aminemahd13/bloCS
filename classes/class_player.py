import pygame
from utils.coord_to_screen import screen_to_coord, coord_to_indice
from game.main import jeu , spawn_new_tile
from random import randint
from utils.textures import block_images
from classes.class_vivant import Vivant
from screens.menu import display_menu, display_tips
from screens.loading_screen import display_loading_screen
from resources import resources
from utils.creer_direction import creer_direction
from classes.class_block import DirtBlock, StoneBlock, ObsidianBlock, BedrockBlock



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
        super().__init__(x_spawn = x_spawn , y_spawn = y_spawn , type = "Player" , health = 100 , dx = 10)
        self.running = True
        self.loaded_game = False
        self.screen = None
        self.map = "Mine"
        self.in_game = False
        self.name = name
        self.height_screen = height_screen
        self.width_screen = width_screen
        self.x_screen = width_screen // 2 - self.taille_block // 2
        self.y_screen = height_screen // 2 - self.taille_block
        self.is_playing_2048 = False
        self.changed = False
        self.grille = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        self.mining = False
        self.dict_touches = {"right" : False , "left" : False , "up" : False , "echap" : False , "number" : 1 , "click" : None}
        self.hist_touches = {"right" : False , "left" : False , "echap" : False}
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
    
    def play_2048(self):
        if self.is_playing_2048:
            keys = []
            for int_key in self.inventory_tuiles.keys():
                if self.inventory_tuiles[int_key]>0:
                    keys.append([int(int_key),self.inventory_tuiles[int_key]])
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
            self.is_playing_2048 = jeu(self.grille , self.hist_touches , self.dict_touches)
        
        if self.is_playing_2048:
            self.in_game = True
        elif self.in_game:
            if not self.dict_touches["echap"]:
                self.in_game = False
        else:
            self.in_game = False

        if not self.in_game and self.dict_touches["echap"] and not self.hist_touches["close"]: # Si on clique sur échap, le jeu se ferme
            self.running = False
        else:
            self.running = True
        
    def do_events(self , background):
        if self.loaded_game:
            if self.dict_touches["click"] is not None:
                self.mouse_click(background = background)
            for event in pygame.event.get():
                if event.type == self.RESET_MINING_EVENT:
                    self.mining = False
                    pygame.time.set_timer(self.RESET_MINING_EVENT, 0)  # Stop the timer
            self.running = True
    
    def mouse_click(self , background):
        if self.is_playing_2048:
            x_screen, y_screen = self.dict_touches["click"][0] , self.dict_touches["click"][1]
            if 50 <= x_screen <= 250 and 50 <= y_screen <= 110:  # Clic sur le bouton Quitter
                self.is_playing_2048 = False
        else:
            self.mining_or_breaking(background = background)
    
    def tuile_max(self):
        m = 0
        for ligne in self.grille:
            for tuile in ligne:
                m = max(m , tuile)
        return m
    
    def change_map(self):
        if self.loaded_game:
            if 38 * 40 <= self.x_left() and self.x_right() < 40 * 40 and 6 * 40 == self.y_up():
                if not self.changed:
                        if self.map == "Mine":
                            self.map = "Maison"
                        elif self.map == "Maison":
                            self.map = "Mine"
                        self.changed = True
            elif 38 * 40 > self.x_right() or self.x_left() >= 40 * 40 or self.y_down() < 5 * 40 or self.y_up() >= 7 * 40:
                self.changed = False
    
    def act_hist_touches(self):
        self.hist_touches["close"] = self.dict_touches["echap"]
        self.hist_touches["right"] = self.dict_touches["right"]
        self.hist_touches["left"] = self.dict_touches["left"]
        self.hist_touches["up"] = self.dict_touches["up"]
        key_get_number = self.dict_touches["number"]
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
                    self.skin_name = "Mining Right"
                elif tuile_max in [16 , 32]:
                    self.skin_name = "Mining Right Grey"
                elif tuile_max in [64 , 128]:
                    self.skin_name = "Mining Right Gold"
                else:
                    self.skin_name = "Mining Right Purple"
                
            elif self.direction_skin == "left":
                if tuile_max in [0 , 2 , 4 , 8]:
                    self.skin_name = "Mining Left"
                elif tuile_max in [16 , 32]:
                    self.skin_name = "Mining Left Grey"
                elif tuile_max in [64 , 128]:
                    self.skin_name = "Mining Left Gold"
                else:
                    self.skin_name = "Mining Left Purple"
                
    def move(self):
        if not self.is_playing_2048 and self.loaded_game:
            #Change la diection du joueur
            self.act_direction()
            
            # On regarde si le joueur est en plein saut et on actualise sa data
            self.check_if_jumping()
                    
            # Changement du skin
            self.change_skin()
                
            # Déplacement du perso
            self.deplacer_perso()
    
    def mining_or_breaking(self , background):
        x_screen, y_screen = self.dict_touches["click"][0] , self.dict_touches["click"][1] #Position du click sur l'écran
        #On converti ces coordonnées en coordonnées relatives au background (en px)
        x , y = screen_to_coord(x_screen = x_screen , y_screen = y_screen , player = self)
        x_indice , y_indice = coord_to_indice(x = x , y = y)
        if self.x_left() - 80 <= x <= self.x_right() + 80 and self.y_up() - 80 <= y <= self.y_down() + 80:
            #Si on est dans une fenêtre de 2 blocs sur les côtés
            if self.dict_touches["click"][2] == 1 and not (self.x_left()<=x<=self.x_right() and self.y_up()<=y<=self.y_down()):  # Left click to place a block
                if x_indice*40+40-1<self.x_left() or x_indice*40>self.x_right() or y_indice*40>self.y_down() or y_indice*40+40-1<self.y_up():
                    selected_block_type = self.block_types[self.selected_block - 1] #Type de bloc sélectionné
                    if self.inventory[selected_block_type] > 0: #Si on en a dans notre inventaire
                        new_block = eval(f"{selected_block_type}Block(x_indice = x_indice , y_indice = y_indice)") #Création de l'objet block
                        if background.add_block(new_block , self.map): #Si le bloc a été placé
                                self.remove_inventory(selected_block_type) #On l'enlève de l'inventaire
            elif self.dict_touches["click"][2] == 3:  # Right click to remove a block
                added = False
                for key , values in background.dict_block[self.map].items():
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
                    
    
    def add_inventory(self,item) -> None:
        """Add item to the inventory"""
        self.inventory[item] += 1
       
        
    def remove_inventory(self,item) -> None:
        """Remove item to the inventory"""
        self.inventory[item] -= 1


    def add_inventory_tuiles(self , value):
        self.inventory_tuiles[str(value)] += 1
    
    def remove_inventory_tuiles(self , value):
        self.inventory_tuiles[str(value)] -= 1
    
    def act_direction(self):
        if self.dict_touches["right"] and (not self.hist_touches["right"] or not self.dict_touches["left"]):
            self.direction = "right"
        elif self.dict_touches["left"] and (not self.hist_touches["left"] or not self.dict_touches["right"]):
            self.direction = "left"
        else:
            self.direction = None
        self.wanna_jump = self.dict_touches["up"]
        self.act_hist_touches()
    
    def crea_data(self):
        return {
            "name" : self.name,
            "loaded_game" : self.loaded_game,
            "map" : self.map,
            "is_playing_2048" : self.is_playing_2048,
            "grille" : self.grille,
            "selected_block" : self.selected_block,
            "inventory" : self.inventory,
            "skin_name" : self.skin_name,
            "health" : self.health,
            "x" : self.x,
            "y" : self.y,
            "running" : self.running
        }
    
    
"""
Utilisation

player = Player(height_screen : int , width_screen : int , x_spawn : int , y_spawn : int , name : str)
x_spawn = indice bloc en haut de spawn
y_spawn = indice bloc en haut de spawn
height_screen , width_screen : paramètres de l'écran
name : nom

player.render(screen , player2)
Affiche le joueur sur l'écran du joueur2, et son inventaire

player.y_up(), player.y_down(), player.x_left(), player.x_right()
Coordonnées des pixels au bord du joueur

player.move()
Fait bouger le joueur et changer le skin

player.take_damage(damage)
Attaque le joueur. Renvoie True s'il est mort

player.add_inventory(item)
Ajoute 1 item dans l'inventaire

player.remove_inventory(item)
Enlève 1 item dans l'inventaire

player.add_inventory_tuiles(value)
Ajoute 1 tuile value dans l'inventaire

player.remove_inventory_tuiles(value)
Enlève 1 tuile value dans l'inventaire

player.change_map(background)
Change la map du background

player.do_events(background)
Regarde les clics de souris
Renvoie True si le jeu continue, False sinon

player.block_near
liste de blocs aux alentours du joueur
"""








