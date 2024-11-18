import os 

class player():
    def __init__(self,name: str="Player 1", coordinates : list = [0,0], skin=os.path.join("game","player.png"), inventory :list = [],health: int=100):
        # [x,y] à changer en fonction du milieu de la map
        """Initializes the player
        name --> string, name of the player
        coordinates --> list of 2 integers [x,y] if coordinates = None then the player will be placed at the center of the map
        skin --> string, path to the skin of the player
        inventory --> list of items in the inventory
        health --> life points of the player
        """
        self.name = name 
        self.coordinates = coordinates 
        self.inventory = inventory 
        self.health = health 
        self.skin = skin

    


#####################Exemple d'utilisation#####################
Player=player("Player 1",[0,0],os.path.join("game","player.png"),[],100)
print(Player.name)
print(Player.coordinates)
print(Player.inventory)
print(Player.health)
print(Player.skin)

        
        

        
        
        
        
        
        