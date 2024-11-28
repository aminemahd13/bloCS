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
        self.dict_touches = {"right" : False , "left" : False , "up" : False , "echap" : False , "number" : 1}
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
    
    def initialize(self):
        # Screen dimensions
        SCREEN_WIDTH = self.width_screen
        SCREEN_HEIGHT = self.height_screen

        # Create the game screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("bloCS")
        # Initialize mixer for background music
        pygame.mixer.init()

        # Display the menu
        while True:
            choice = display_menu(self.screen)
            if choice == "Start Game":
                self.loaded_game = True
                break
            elif choice == "Tips":
                display_tips(self.screen)
            elif choice == "Quit":
                pygame.quit()
                exit()

        # Display the loading screen
        display_loading_screen(self.screen)

        # Play game background music
        pygame.mixer.music.load(resources("assets/audio/game.mp3"))
        pygame.mixer.music.play(-1)  # Loop the music
        return self.loaded_game                    
                    
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
            self.is_playing_2048 = jeu(self.grille , self.screen , self.hist_touches)
        
        if self.is_playing_2048:
            self.in_game = True
        elif self.in_game:
            if not self.dict_touches["echap"]:
                self.in_game = False
        else:
            self.in_game = False

        if not self.in_game and self.dict_touches["echap"] and not self.hist_touches["close"]: # Si on clique sur échap, le jeu se ferme
            return False
        return True
    
    def draw_inventory(self):
        font = pygame.font.Font(None, int(36 * self.screen.get_height() / 1080))
        x_offset = 10
        y_offset = 10
        for i, block_type in enumerate(self.block_types):
            block_image = block_images[block_type]
            if i+1 == self.selected_block:
                pygame.draw.rect(self.screen, (0, 255, 0), (x_offset + i * int(90 * self.screen.get_height() / 1080) - 5, y_offset - 5, int(50 * self.screen.get_height() / 1080), int(50 * self.screen.get_height() / 1080)), 3)
            self.screen.blit(block_image, (x_offset + i * int(90 * self.screen.get_height() / 1080), y_offset))
            n = self.inventory[block_type]
            text = font.render(str(n), True, (0, 0, 0))
            self.screen.blit(text, (x_offset + i * int(90 * self.screen.get_height() / 1080) + int(45 * self.screen.get_height() / 1080), y_offset + int(10 * self.screen.get_height() / 1080)))
    
    def close(self):
       # Quit Pygame
        pygame.mixer.music.stop()
        pygame.quit()
    
    
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








