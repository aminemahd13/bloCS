import os 
import pygame


class Player:
    def __init__(self , height_screen : int , width_screen : int , name : str = "Player 1"):
        # [x,y] à changer en fonction du milieu de la map
        """Initializes the player
        name --> string, name of the player
        coordinates --> list of 2 integers [x,y] if coordinates = None then the player will be placed at the center of the map
        skin --> string, path to the skin of the player
        inventory --> list of items in the inventory
        health --> life points of the player
        """
        self.jump = False
        self.name = name
        self.taille_block = 40
        self.x = height_screen // 2 - self.taille_block // 2
        self.y = width_screen // 2 - self.taille_block
        self.direction = "right"
        self.stade = 0
        
        self.inventory = []
        self.health = 100
        self.skin_path = os.path.join("game","assets","graphics","standing_right.png")
        self.skin = pygame.image.load(self.skin_path)
        

    
    def change_skin(self , keyboard_direction : str , mining : bool) -> None:
        
        """Player Movement
        keyboard_jump --> True or False if jump
        keyboard_direction --> string, direction of the player
        mining --> True or False if mining
        we change skin depending on the direction or if he jump or mining
        """
        #Not mining
        if not mining:
            #Jumping
            if self.jump:
                if keyboard_direction == "right" or (keyboard_direction is None and self.direction == "right"):
                    self.skin_path = os.path.join("game" , "assets" , "graphics" , "jumping_right.png")
                    self.skin = pygame.image.load(self.skin_path)
                    
                elif keyboard_direction == "left" or (keyboard_direction is None and self.direction == "left"):
                    self.skin_path = os.path.join("game" , "assets" , "graphics" , "jumping_left.png")
                    self.skin = pygame.image.load(self.skin_path)
            
            #Not jumping
            else:
                #Changing stade --> moving right or left if he was in opposite direction
                if keyboard_direction == self.direction:
                    self.stade = 1 - self.stade
                else:
                    self.stade = 0
                
                #Moving right
                if keyboard_direction == "right" or (keyboard_direction is None and self.direction == "right"):
                    if self.stade == 1:
                        self.skin_path = os.path.join("game" , "assets" , "graphics" , "walking_right.png")
                        self.skin = pygame.image.load(self.skin_path)
                    else :
                        self.skin_path = os.path.join("game" , "assets" , "graphics" , "standing_right.png")
                        self.skin = pygame.image.load(self.skin_path)
                
                #Moving left  
                elif keyboard_direction == "left" or (keyboard_direction is None and self.direction == "left"):
                    if self.stade == 1 :
                        self.skin_path = os.path.join("game" , "assets" , "graphics" , "walking_left.png")
                        self.skin = pygame.image.load(self.skin_path)
                    else :
                        self.skin_path = os.path.join("game" , "assets" , "graphics" , "standing_left.png")
                        self.skin = pygame.image.load(self.skin_path)
            
        
        #Mining
        else:
            if keyboard_direction == "right":
                self.skin_path = os.path.join("game" , "assets" , "graphics" , "mining_right.png")
                self.skin = pygame.image.load(self.skin_path)
                
            elif keyboard_direction == "left":
                self.skin_path = os.path.join("game" , "assets" , "graphics" , "mining_left.png")
                self.skin = pygame.image.load(self.skin_path)
                
            elif self.direction == "left":
                self.skin_path = os.path.join("game" , "assets" , "graphics" , "mining_left.png")
                self.skin = pygame.image.load(self.skin_path)
                
            elif self.direction == "right":
                self.skin_path = os.path.join("game" , "assets" , "graphics" , "mining_right.png")
                self.skin = pygame.image.load(self.skin_path)
                
        
        
        
    
            
        


#####################Exemple d'utilisation#####################
player=Player(height_screen = 1920 , width_screen = 1080 , name = "Player 1")
print(player.name)
print(player.x)
print(player.y)
print(player.inventory)
print(player.health)
print(player.skin)

#Change skin première fois
player.change_skin(keyboard_direction = "right" , mining = False)
print(player.skin_path)
#Change skin deuxième fois --> animation
player.change_skin(keyboard_direction = "right" , mining = False)
print(player.skin_path)

player.change_skin(keyboard_direction = "right" , mining = True)
print(player.skin_path)






        
        

        
        
        
        
        
        