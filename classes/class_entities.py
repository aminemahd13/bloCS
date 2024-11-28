from classes.class_mob import Zombie
from classes.class_player import Player

class Entities:
    def __init__(self):
        self.players_dict = {}
        self.player_names = []
        self.mobs_dict = {
            "Zombie" : []
        }
    
    def add_player(self , name , height_screen , width_screen): 
        while name in self.player_names:
            name = name + "0"
        self.players_dict[name] = Player(height_screen = height_screen , width_screen = width_screen , name = name)
        self.player_names.append(name)
        return name
    
    def remove_player(self , name):
        self.players_dict.pop(name)
        self.player_names.remove(name)
    
    def add_mob(self , type , map , x_spawn , y_spawn):
        #A changer, x_spawn et y_spawn dépendent de plein de choses
        mob = eval(f"{type}(x_spawn = x_spawn , y_spawn = y_spawn)")
        mob.map = map
        self.mobs_dict[type].append(mob)
    
    def remove_mob(self , type , map):
        for i , mob in enumerate(self.mobs_dict[type]):
            if mob.map == map:
                self.mobs_dict[type].pop(i)
                return True
        return False
    
    def render(self , player_name , background):
        player = self.players_dict[player_name]
        if not player.is_playing_2048:
        # Render the background and players
            background.render(player = player) # Affiche le background avec les blocs
            for all_players in self.players_dict.values():
                if all_players.loaded_game:
                    all_players.render(player)
            for all_types in self.mobs_dict.values():
                for mob in all_types:
                    mob.render(player)
            player.draw_inventory()
    
    def initialize(self , player_name):
        return self.players_dict[player_name].initialize()
    
    def close(self , player_name):
        self.players_dict[player_name].close()
        self.remove_player(player_name)