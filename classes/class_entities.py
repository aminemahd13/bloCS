from classes.class_mob import Zombie
from classes.class_player import Player

class Entities:
    def __init__(self):
        self.players_dict = {}
        self.player_names = []
        self.mobs_dict = {
            "Zombie" : []
        }
        self.mob_id = 0
    
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
        mob.id = self.mob_id
        self.mob_id += 1
        self.mobs_dict[type].append(mob)
    
    def remove_mob(self , type , map):
        for i , mob in enumerate(self.mobs_dict[type]):
            if mob.map == map:
                self.mobs_dict[type].pop(i)
                return True
        return False
    
    def move(self):
        for all_players in self.players_dict.values():
            if all_players.loaded_game:
                all_players.move()
                all_players.change_map()
        for all_types in self.mobs_dict.values():
            for mob in all_types:
                mob.move(self.players_dict)
    
    def play(self , background):
        background.crea_block_near(self.players_dict , self.mobs_dict)
        for player in self.players_dict.values():
            player.do_events(background = background)
            player.play_2048()
    
    def crea_data(self):
        data = {
            "Player" : {},
            "Mob" : {}
                }
        for all_players in self.players_dict.values():
            data["Player"][all_players.name] = all_players.crea_data()
        for all_types in self.mobs_dict.values():
            for mob in all_types:
                data["Mob"][mob.id] = mob.crea_data()
        
        return data