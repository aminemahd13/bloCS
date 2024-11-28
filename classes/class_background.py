from classes.class_block import Block, DirtBlock, StoneBlock, WoodBlock, BedrockBlock, ObsidianBlock , Wood1Block , Wood2Block , DoorupBlock , DoordownBlock, TuileBlock , GameBlock
from classes.class_player import Player
from utils.coord_to_screen import coord_to_screen, coord_to_indice, indice_to_screen
from utils.lists_blocks import block_lists
from utils.house_list import house_blocks
from utils.textures import texture_background



class Background:
    def __init__(self):
        self.mode = 1
        dict_block_background = {}
        dict_block_house = {}
        self.dict_block = {}
        self.__taille_block = 40
        self.back_texture = texture_background
        
        for block_type in ["Game" , "Wood1" , "Doorup" , "Doordown"]:
            for coord in house_blocks[block_type]:
                dict_block_house[coord] = eval(f"{block_type}Block(x_indice = coord[0] , y_indice = coord[1])")
        for coord in house_blocks["Wood2"]:
            dict_block_house[coord] = Wood2Block(x_indice = coord[0] , y_indice = coord[1] , is_solid = True)
                
        for block_type in ["Dirt" , "Stone" , "Wood2" , "Wood1" , "Doorup" , "Doordown" , "Obsidian" , "Wood" , "Bedrock"]:
            for coord in block_lists[block_type]:
                dict_block_background[coord] = eval(f"{block_type}Block(x_indice = coord[0] , y_indice = coord[1])")
        
        self.dict_block["Mine"] = dict_block_background
        self.dict_block["Maison"] = dict_block_house
    
      
    def add_block(self, type , map , x : int = None , y : int = None , x_indice : int = None , y_indice : int = None) -> bool:
        """
        Ajoute un bloc dans le background.
        Enlève le bloc qu'il y avait de base.
        """
        if x_indice is None:
            x_indice , y_indice = coord_to_indice(x = x , y = y)
        coord = [x_indice , y_indice]
        block_here = False
        if coord in self.dict_block[map]:
            block_here = True
        self.dict_block[map][coord] = eval(f"{type}Block(x_indice = x_indice , y_indice = y_indice)")
        return block_here

    def damage_block(self , damage : int, player : Player , map : str , x : int = None , y : int = None , x_indice : int = None , y_indice : int = None) -> bool:
        """
        Attaque le bloc se situant en x , y.
        S'il y avait un bloc qui a été détruit, renvoie True.
        Sinon, renvoie False.
        """
        if x_indice is None:
            x_indice , y_indice = coord_to_indice(x = x , y = y)
        coord = [x_indice , y_indice]
        if coord in self.dict_block[map]:
            block = self.dict_block[map][coord]
            if block.take_damage(damage , player.tuile_max()):
                self.dict_block[map].pop(coord)
                player.inventory[block.type] += 1
                return True
        return False
    
    
    def render(self, player : Player) -> None:
        """
        Affiche le background.
        """
        # Clear the screen
        player.screen.fill((255,255,255))
        if self.mode == 1:
            x_screen , y_screen = indice_to_screen(x_indice = -2 * 39 , y_indice = 0 , player = player)
            player.screen.blit(self.back_texture, (x_screen , y_screen))
        for block in self.dict_block[player.map].values():
            x_screen , y_screen = coord_to_screen(x = block.x , y = block.y , player = player)
            if 1 - self.__taille_block <= x_screen <= player.width_screen and 1 - self.__taille_block <= y_screen <= player.height_screen:
                #On affiche uniquement les blocs qui se situent dans la map
                block.render(player = player)
    
    def crea_block_near(self , dict_player : dict , dict_mob : dict):
        map_players = {}
        map_mobs = {
            "Mine" : [],
            "Maison" : []
        }
        
        for player in dict_player.values():
            player.block_near = []
            if player.map not in map_players:
                map_players[player.map] = []
            map_players[player.map].append(player)
        for types in dict_mob.values():
            for mob in types:
                mob.block_near = []
                map_mobs[mob.map].append(mob)
        
        for map in map_players:
            for block in self.dict_block[map].values():
                for player in map_players[map]:
                    if block.x_right() >= player.x_left() - 20 and block.x_left() <= player.x_right() + 20 and player.y_up() - 50 <= block.y_down() and block.y_up()<= player.y_down() + 50:
                        player.block_near.append(block)
                for mob in map_mobs[map]:
                    if block.x_right() >= mob.x_left() - 20 and block.x_left() <= mob.x_right() + 20 and mob.y_up() - 50 <= block.y_down() and block.y_up()<= mob.y_down() + 50:
                        mob.block_near.append(block)


"""

# Pygame initialization
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Create the game screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Terraria-like Game Test")

# Colors
WHITE = (255, 255, 255)

background = Background(width = 1920 , height = 1080)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(WHITE)

    # Render the background and blocks
    background.render(screen)

    # Example interaction (move blocks or damage a block)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        background.right(5)
    if keys[pygame.K_LEFT]:
        background.left(5)
    if keys[pygame.K_DOWN]:
        background.down(5)
    if keys[pygame.K_UP]:
        background.up(5)

    # Update the screen
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
"""

"""
Utilisation



Initialisation du background :
background = Background(width : int , height : int)



Déplacer le joueur à droite (<=> déplacer le background à gauche) de deplacement pixels :
background.right(deplacement : int) -> None



Déplacer le joueur à gauche (<=> déplacer le background à droite) de deplacement pixels :
background.left(deplacement : int) -> None



Déplacer le joueur en haut (<=> déplacer le background en bas) de deplacement pixels :
background.up(deplacement : int) -> None



Déplacer le joueur à bas (<=> déplacer le background en haut) de deplacement pixels :
background.down(deplacement : int) -> None



background.add_block(block : Block , decalage_auto : bool = True) -> bool
Ajoute un bloc en x,y.
Renvoie True si le bloc a été placé (s'il y avait pas de bloc ici), False sinon.

Remarque : Imaginons qu'un bloc peut être placé en coordonnées haut-gauche (0,0) pour avoir le bon décalage
avec le reste de la map. Si on veut ajouter le bloc en (1,1), ça va automatiquement le mettre
en (0,0) pour avoir le bon décalage avec le reste de la map.
Cette option peut être désactivée.



background.damage_block(x : int , y : int , damage : int) -> bool
Attaque le bloc, s'il existe, en x,y.
Renvoie True s'il y avait un bloc qui a été détruit, False sinon.



background.check_block(x : int , y : int) -> Block
Renvoie le bloc se situant en x,y.
Renvoie None s'il n'y a pas de block.



background.render() -> None
Affiche le background.

"""