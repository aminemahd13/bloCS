import os 
import pygame
import keyboard



class player():
    def __init__(self,height_screen,width_screen,name: str="Player 1"):
        # [x,y] à changer en fonction du milieu de la map
        """Initializes the player
        name --> string, name of the player
        coordinates --> list of 2 integers [x,y] if coordinates = None then the player will be placed at the center of the map
        skin --> string, path to the skin of the player
        inventory --> list of items in the inventory
        health --> life points of the player
        """
        
        self.__height = height_screen
        self.__width = width_screen
        self.name = name 
        self.taille_block=40
        self.x= height_screen//2 - self.taille_block//2
        self.y = width_screen//2 - self.taille_block
        self.direction = "right"
        self.__stade = 0
        self.jump = False
        
        self.inventory = []
        self.health = 100
        self.skin_path = os.path.join("game","assets","graphics","standing_right.png")
        self.skin = pygame.image.load(self.skin_path)
        

    
    def change_skin(self,keyboard_jump,keyboard_direction,mining):
        
        """Player Movement
        keyboard_jump --> True or False if jump
        keyboard_direction --> string, direction of the player
        mining --> True or False if mining
        we change skin depending on the direction or if he jump or mining
        """
        
        #Jumping
        if keyboard_jump and keyboard_direction == "right" and mining==False:
            self.skin_path = os.path.join("game","assets","graphics","jumping_right.png")
            self.skin = pygame.image.load(self.skin_path)
            
        elif keyboard_jump and keyboard_direction == "left" and mining==False:
            self.skin_path = os.path.join("game","assets","graphics","jumping_left.png")
            self.skin = pygame.image.load(self.skin_path)
        
        #Changing stade --> moving right or left if he was in opposite direction
        if keyboard_jump==False and keyboard_direction == "left" and self.direction == "right":
            self.stade=0
        
        elif keyboard_jump==False and keyboard_direction == "right" and self.direction == "left":
            self.stade=0
        
        #Moving right
        if keyboard_jump==False and keyboard_direction == "right" and self.direction == "right" and mining==False:
            if self.stade == 0:
                self.stade =1
                self.skin_path = os.path.join("game","assets","graphics","walking_right.png")
                self.skin = pygame.image.load(self.skin_path)
            else :
                self.stade = 0
                self.skin_path = os.path.join("game","assets","graphics","standing_right.png")
                self.skin = pygame.image.load(self.skin_path)
        
        #Moving left  
        elif keyboard_jump==False and keyboard_direction == "left" and self.direction == "left" and mining==False:
            
            if self.stade == 0 :
                self.stade =1
                self.skin_path = os.path.join("game","assets","graphics","walking_left.png")
                self.skin = pygame.image.load(self.skin_path)
                
            else :
                self.stade = 0
                self.skin_path = os.path.join("game","assets","graphics","standing_left.png")
                self.skin = pygame.image.load(self.skin_path)
            
        
        #Mining
        if mining:
            
            if keyboard_direction == "right":
                self.skin_path = os.path.join("game","assets","graphics","mining_right.png")
                self.skin = pygame.image.load(self.skin_path)
                
            elif keyboard_direction =="left":
                self.skin_path = os.path.join("game","assets","graphics","mining_left.png")
                self.skin = pygame.image.load(self.skin_path)
                
            elif self.direction == "left":
                self.skin_path = os.path.join("game","assets","graphics","mining_left.png")
                self.skin = pygame.image.load(self.skin_path)
                
            elif self.direction =="right":
                self.skin_path = os.path.join("game","assets","graphics","mining_right.png")
                self.skin = pygame.image.load(self.skin_path)
                
        
        
        
    
            
        


#####################Exemple d'utilisation#####################
Player=player("Player 1",[0,0],os.path.join("game","player.png"),[],100)
print(Player.name)
print(Player.coordinates)
print(Player.inventory)
print(Player.health)
print(Player.skin)

        
        

        
        
        
        
        
        