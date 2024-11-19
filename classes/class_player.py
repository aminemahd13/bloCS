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
        self.mining = False
        self.taille_block = 40
        self.x = height_screen // 2 - self.taille_block // 2
        self.y = width_screen // 2 - self.taille_block
        self.direction = "right"
        self.stade = 0
        
        self.inventory = []
        self.health = 100
        self.skin_path = "assets/graphics/standing_right.png"
        self.skin = pygame.image.load(self.skin_path)
        

    
    def change_skin(self , moving : str) -> None:
        
        """Player Movement
        keyboard_jump --> True or False if jump
        keyboard_direction --> string, direction of the player
        mining --> True or False if mining
        we change skin depending on the direction or if he jump or mining
        """
        #Not mining
        if not self.mining:
            #Jumping
            if self.jump:
                if self.direction == "right":
                    self.skin_path = "assets/graphics/jumping_right.png"
                    self.skin = pygame.image.load(self.skin_path)
                    
                elif self.direction == "left":
                    self.skin_path = "assets/graphics/jumping_left.png"
                    self.skin = pygame.image.load(self.skin_path)
            
            #Not jumping
            else:
                #Changing stade --> moving right or left if he was in opposite direction
                if moving:
                    if self.stade == 20:
                        self.stade = 1
                    else:
                        self.stade += 1
                else:
                    self.stade=0

                
                #Moving right
                if self.direction == "right":
                    if self.stade <= 20//2:
                        self.skin_path = "assets/graphics/walking_right.png"
                        self.skin = pygame.image.load(self.skin_path)
                        
                        
                    else :
                        self.skin_path = "assets/graphics/standing_right.png"
                        self.skin = pygame.image.load(self.skin_path)
                        
                    self.direction = "right"       
                        
                
                #Moving left  
                elif self.direction == "left":
                    if self.stade <= 20//2:
                        self.skin_path = "assets/graphics/walking_left.png"
                        self.skin = pygame.image.load(self.skin_path)
                    else :
                        self.skin_path = "assets/graphics/standing_left.png"
                        self.skin = pygame.image.load(self.skin_path)
                    self.direction = "left"   
                        
            
        
        #Mining
        else:
            if self.direction == "right":
                self.skin_path = "assets/graphics/mining_right.png"
                self.skin = pygame.image.load(self.skin_path)
                
            elif self.direction == "left":
                self.skin_path = "assets/graphics/mining_left.png"
                self.skin = pygame.image.load(self.skin_path)
        
        self.skin = pygame.transform.scale(self.skin, (40, 80))
                
        
    def add_inventory(self,item) -> None:
        """Add item to the inventory"""
        self.inventory.append(item)
        
    def remove_inventory(self,item) -> None:
        """Remove item to the inventory"""
        self.inventory.remove(item)
    
    def render(self , screen):
        if self.skin:
            screen_x = self.x
            screen_y = self.y
            screen.blit(self.skin, (screen_x, screen_y))
            
        
            
        
"""

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
#Change skin mining 
player.change_skin(keyboard_direction = "right" , mining = True)
print(player.skin_path)


"""

        
        

        
        
        
        
        