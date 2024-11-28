from classes.class_mob import Zombie
from classes.class_player import Player

class Entities:
    def __init__(self):
        self.players_dict = {}
        self.mobs_dict = {}
    
    def add_player(self , id):
        self.players_dict[id] = Player(height_screen = 1080 , width_screen = 1920 , name = "Player 1")
    
    def remove_player(self , id):
        self.players_dict.pop(id)
    
    def add_mob(self , type , id):
        mob = eval(f"{type}()")
        self.mobs_dict[id] = mob
    
    def remove_mob(self , id):
        self.mobs_dict.pop(id)
    
    def render(self , player_name , background):
        player = self.players_dict[player_name]
        if not player.is_playing_2048:
        # Render the background and players
            background.render(player = player) # Affiche le background avec les blocs
            for all_players in self.players_dict.values():
                if all_players.loaded_game:
                    all_players.render(player)
            for mob in self.mobs_dict.values():
                mob.render(player)
            player.draw_inventory()
    
    def initialize(self , player_name):
        return self.players_dict[player_name].initialize()
    
    def close(self , player_name):
        self.players_dict[player_name].close()
    
    def recup_data(self , received_data):
        server_players_id = [player_id for player_id in received_data["Player"].keys()]
        local_players_id = [player_id for player_id in self.players_dict.keys()]
        
        for player_id in server_players_id:
            if player_id not in local_players_id:
                self.add_player(player_id)
        
        for player_id in local_players_id:
            if player_id not in server_players_id:
                self.remove_player(player_id)
        
        server_mobs_id = [mob_id for mob_id in received_data["Mob"].keys()]
        local_mobs_id = [mob_id for mob_id in self.mobs_dict.keys()]
        
        for mob_id in server_mobs_id:
            if mob_id not in local_mobs_id:
                self.add_mob(type = received_data["Mob"][mob_id]["type"] , id = mob_id)
        
        for mob_id in local_mobs_id:
            if mob_id not in server_mobs_id:
                self.remove_mob(mob_id)
        
        
        for player_id , player_data in received_data["Player"].items():
            for prop_id , prop in player_data.items():
                eval(f"self.players_dict[player_id].{prop_id} = {prop}")
            self.players_dict[player_id].change_skin()
        
        for mob_id , mob_data in received_data["Mob"].items():
            for prop_id , prop in mob_data.items():
                eval(f"self.mobs_dict[mob_id].{prop_id} = {prop}")
            self.mobs_dict[mob_id].change_skin()