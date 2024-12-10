from classes.class_block import Block, DirtBlock, StoneBlock, WoodBlock, BedrockBlock, ObsidianBlock , Wood1Block , Wood2Block , DoorupBlock , DoordownBlock, TuileBlock , GameBlock
from classes.class_player import Player
from utils.coord_to_screen import coord_to_indice
from utils.lists_blocks import block_lists
from utils.house_list import house_blocks



class Background:
    def __init__(self):
        self.mode = 1
        dict_block_background = {}
        dict_block_house = {}
        self.dict_block = {}
        
        for block_type in ["Game" , "Wood1" , "Doorup" , "Doordown"]:
            for coord in house_blocks[block_type]:
                coord = (coord[0] , coord[1])
                dict_block_house[coord] = eval(f"{block_type}Block(x_indice = coord[0] , y_indice = coord[1])")
        for coord in house_blocks["Wood2"]:
            coord = (coord[0] , coord[1])
            dict_block_house[coord] = Wood2Block(x_indice = coord[0] , y_indice = coord[1] , is_solid = True)
                
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
        if coord in self.dict_block[map]:
            return False
        else:
            self.dict_block[map][coord] = eval(f"{type}Block(x_indice = x_indice , y_indice = y_indice)")
            return True

    def damage_block(self , damage : int, player : Player , map : str , x : int = None , y : int = None , x_indice : int = None , y_indice : int = None) -> bool:
        """
        Attaque le bloc se situant en x , y.
        S'il y avait un bloc qui a été détruit, renvoie True.
        Sinon, renvoie False.
        """
        if x_indice is None:
            x_indice , y_indice = coord_to_indice(x = x , y = y)
        coord = (x_indice , y_indice)
        if coord in self.dict_block[map]:
            block = self.dict_block[map][coord]
            self.logger.debug(f"Player {player.name} damaging block {block.type} at ({x_indice}, {y_indice}) with damage {damage}")
            if block.take_damage(damage , player.tuile_max()):
                self.logger.info(f"Block {block.type} at ({x_indice}, {y_indice}) destroyed by player {player.name}")
                self.dict_block[map].pop(coord)
                player.inventory[block.type] += 1
                return True
        return False
        
    
    def crea_block_near(self , dict_player : dict , dict_mob : dict):
        map_players = {
            "Mine" : [],
            "Maison" : []
        }
        map_mobs = {
            "Mine" : [],
            "Maison" : []
        }
        
        for player in dict_player.values():
            player.block_near = []
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
