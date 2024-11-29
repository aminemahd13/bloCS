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
                coord = (coord[0] , coord[1])
                dict_block_house[coord] = eval(f"{block_type}Block(x_indice = coord[0] , y_indice = coord[1])")
        for coord in house_blocks["Wood2"]:
            coord = (coord[0] , coord[1])
            dict_block_house[coord] = Wood2Block(x_indice = coord[0] , y_indice = coord[1])
                
        for block_type in ["Dirt" , "Stone" , "Wood2" , "Wood1" , "Doorup" , "Doordown" , "Obsidian" , "Wood" , "Bedrock"]:
            for coord in block_lists[block_type]:
                coord = (coord[0] , coord[1])
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
        coord = (x_indice , y_indice)
        block_here = False
        if coord in self.dict_block[map]:
            block_here = True
        self.dict_block[map][coord] = eval(f"{type}Block(x_indice = x_indice , y_indice = y_indice)")
        return block_here
    
    def remove_block(self , map , x : int = None , y : int = None , x_indice : int = None , y_indice : int = None) -> bool:
        """
        Enlève le bloc.
        """
        if x_indice is None:
            x_indice , y_indice = coord_to_indice(x = x , y = y)
        coord = (x_indice , y_indice)
        if coord in self.dict_block[map]:
            self.dict_block[map].pop(coord)
    
    
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
    