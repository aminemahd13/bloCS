import pygame
from game.main import jeu
from utils.textures import block_images
from classes.class_vivant import Vivant
from screens.menu import display_menu, display_tips
from screens.loading_screen import display_loading_screen
from resources import resources
from classes.class_block import DirtBlock, StoneBlock, ObsidianBlock, BedrockBlock
from utils.coord_to_screen import screen_to_coord
from utils.coord_to_screen import coord_to_indice


class Player(Vivant):
    def __init__(self , height_screen : int = 1080 , width_screen : int = 1920 , name : str = "Player 1"):
        super().__init__(type = "Player")
        self.loaded_game = False
        self.screen = None
        self.taille_block = 40
        self.map = "Mine"
        self.name = name
        self.height_screen = height_screen
        self.width_screen = width_screen
        self.x_screen = width_screen // 2 - self.taille_block // 2
        self.y_screen = height_screen // 2 - self.taille_block
        self.is_playing_2048 = False
        self.grille = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        self.dict_touches = {"right" : False , "left" : False , "up" : False , "echap" : False , "number" : 1}
        self.hist_touches = {"right" : False , "left" : False , "echap" : False}
        self.selected_block = 1
        self.block_types = ["Dirt", "Stone", "Obsidian", "Bedrock"]
        
        self.inventory = {
            "Dirt" : 10,
            "Stone" : 0,
            "Obsidian" : 0,
            "Bedrock" : 0
        }
    
    def initialize(self):
        self.loaded_game = True
        # Create the game screen
        self.screen = pygame.display.set_mode((self.width_screen, self.height_screen))
        pygame.display.set_caption("bloCS")
        # Initialize mixer for background music
        pygame.mixer.init()
        # Play game background music
        pygame.mixer.music.load(resources("assets/audio/game.mp3"))
        pygame.mixer.music.play(-1)  # Loop the music
    
                    
    def play_2048(self):
        if self.is_playing_2048:
            jeu(self.grille , self.screen) #On affiche la grille
    
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
    
    def update_from_data(self, data):
        self.name = data.get("name", self.name)
        self.loaded_game = data.get("loaded_game", self.loaded_game)
        self.map = data.get("map", self.map)
        self.is_playing_2048 = data.get("is_playing_2048", self.is_playing_2048)
        self.grille = data.get("grille", self.grille)
        self.selected_block = data.get("selected_block", self.selected_block)
        self.inventory = data.get("inventory", self.inventory)
        self.skin_name = data.get("skin_name", self.skin_name)
        self.health = data.get("health", self.health)
        self.x = data.get("x", self.x)
        self.y = data.get("y", self.y)
        self.running = data.get("running", self.running)

    def mining_or_breaking(self, background):
        x_screen, y_screen = self.dict_touches["click"][0], self.dict_touches["click"][1]  # Position du click sur l'écran
        # Convertir ces coordonnées en coordonnées relatives au background (en px)
        x, y = screen_to_coord(x_screen=x_screen, y_screen=y_screen, player=self)
        x_indice, y_indice = coord_to_indice(x=x, y=y)
        if self.x_left() - 80 <= x <= self.x_right() + 80 and self.y_up() - 80 <= y <= self.y_down() + 80:
            # Si on est dans une fenêtre de 2 blocs sur les côtés
            if self.dict_touches["click"][2] == 1 and not (self.x_left() <= x <= self.x_right() and self.y_up() <= y <= self.y_down()):
                # Left click to place a block
                selected_block_type = self.block_types[self.selected_block - 1]  # Type de bloc sélectionné
                if self.inventory.get(selected_block_type, 0) > 0:  # Si on en a dans notre inventaire
                    new_block = eval(f"{selected_block_type}Block(x_indice=x_indice, y_indice=y_indice)")  # Création de l'objet block
                    if background.add_block(new_block, self.map):
                        # Si le bloc a été placé
                        self.remove_inventory(selected_block_type)  # On l'enlève de l'inventaire
            elif self.dict_touches["click"][2] == 3:
                # Right click to remove a block
                block = background.dict_block[self.map].get((x_indice, y_indice))
                if block and block.type != "Game":
                    if block.take_damage(damage=100, tuile_max=self.tuile_max()):
                        background.remove_block(self.map, x_indice=x_indice, y_indice=y_indice)
                        if block.type == "Tuile":
                            self.inventory_tuiles[str(block.value)] += 1
                        else:
                            self.add_inventory(block.type)
                        self.mining = True
                        pygame.time.set_timer(self.RESET_MINING_EVENT, 350)  # Set a timer for 0.35 seconds
                    elif block.type == "Game":
                        self.is_playing_2048 = True

