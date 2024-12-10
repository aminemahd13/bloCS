from classes.class_mob import Zombie
from classes.class_player import Player
from utils.calcul_teinte import calculer_teinte

class Entities:
    def __init__(self):
        self.players_dict = {}
        self.mobs_dict = {}
        self.fps = 60
    
    def add_player(self , name , player_id , height , width):
        self.players_dict[player_id] = Player(height_screen=height, width_screen=width, name=name)
    
    def remove_player(self , player_id):
        if player_id in self.players_dict:
            del self.players_dict[player_id]
    
    def add_mob(self , type , map , x_spawn , y_spawn):
        self.mob_id += 1
        mob = eval(f"{type}(x_spawn = x_spawn , y_spawn = y_spawn)")
        mob.map = map
        mob.id = self.mob_id
        self.mobs_dict[mob.id] = mob
    
    def remove_mob(self , mob_id):
        self.mobs_dict.pop(mob_id)
    
    def move(self):
        # Implement entity movement logic
        pass
    
    def play(self , background):
        for player in self.players_dict.values():
            player.move()
        # Implement mob behavior if applicable
    
    def crea_data(self):
        return {
            "Player": {pid: p.crea_data() for pid, p in self.players_dict.items()},
            "Mob": {mid: m.crea_data() for mid, m in self.mobs_dict.items()}
        }
    
    def render(self, player_id, background):
        # Implement rendering logic
        pass