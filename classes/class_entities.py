from classes.class_mob import Zombie
from classes.class_player import Player

class Entities:
    def __init__(self):
        self.players_dict = {}
        self.mobs_dict = {}
        self.mob_id = 0
        self.player_id = 0
    
    def add_player(self , name , height_screen , width_screen):
        self.player_id += 1
        player = Player(height_screen = height_screen , width_screen = width_screen , name = name)
        player.id = self.player_id
        player.map = "Mine"
        self.players_dict[self.player_id] = player
        return self.player_id
    
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
    
    def recup_and_crea_data(self , received_data):
        data = {
            "Player" : {},
            "Mob" : {},
            "Joined" : []
                }
        for player in self.players_dict.values():
            player.dict_touches = received_data[player.id]
        
        for id_wanna_quit in received_data["wanna_quit"]:
            if id_wanna_quit in self.players_dict:
                self.players_dict.pop(id_wanna_quit)
                received_data["wanna_quit"].remove(id_wanna_quit)
        
        for i , wanna_join in enumerate(received_data["wanna_join"]):
            player_id = self.add_player(wanna_join[0] , wanna_join[1] , wanna_join[2])
            received_data["wanna_join"].pop(i)
            #Faire un truc à ajouter dans la liste data["Joined"] avec le joueur qui a rejoint et son identifiant de joueur
        
        for player in self.players_dict.values():
            data["Player"][player.id] = player.crea_data()
        for mob in self.mobs_dict.values():
            data["Mob"][mob.id] = mob.crea_data()
        
        return data