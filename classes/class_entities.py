from classes.class_mob import Zombie
from classes.class_player import Player
from copy import deepcopy

class Entities:
    def __init__(self):
        self.players_dict = {}
        self.mobs_dict = {}
        self.mob_id = 0
    
    def add_player(self , name , player_id , height_screen , width_screen):
        player = Player(height_screen = height_screen , width_screen = width_screen , name = name)
        player.map = "Mine"
        player.id = player_id
        self.players_dict[player_id] = player
    
    def remove_player(self , player_id):
        self.players_dict.pop(player_id)
    
    def add_mob(self , type , map , x_spawn , y_spawn):
        self.mob_id += 1
        mob = eval(f"{type}(x_spawn = x_spawn , y_spawn = y_spawn)")
        mob.map = map
        mob.id = self.mob_id
        self.mobs_dict[mob.id] = mob
    
    def remove_mob(self , mob_id):
        self.mobs_dict.pop(mob_id)
    
    def move(self):
        for all_players in self.players_dict.values():
            if all_players.loaded_game:
                all_players.move()
                all_players.change_map()
        for mob in self.mobs_dict.values():
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
        
        #Enlever le joueur d'identifiant player_id dans le serveur
        #self.players_dict.pop(player_id)
        
        #Ajouter un joueur de nom player_name, dimension d'écran height, width
        #player_id = self.add_player(player_name , height , width)
        #Envoyer player_id à l'utilisateur concerné
        
        for player in self.players_dict.values():
            data["Player"][player.id] = player.crea_data()
        for mob in self.mobs_dict.values():
            data["Mob"][mob.id] = mob.crea_data()
        
        return data