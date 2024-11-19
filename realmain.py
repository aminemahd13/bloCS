import pygame
from classes.class_background import Background
from classes.class_block import DirtBlock, StoneBlock, WoodBlock, BedrockBlock
from classes.class_player import Player
import utils.key_handler as key
import time

# Pygame initialization
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
g = 1200
V0 = 500
dx = 5
compteur_jump = 0
dist_theo=0
dist_real=0

# Colors
WHITE = (255, 255, 255)

# Create the game screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Terraria-like Game Test")

# Initialize the background
background = Background(SCREEN_HEIGHT, SCREEN_WIDTH)

#Create the player
player=Player(height_screen = 1920 , width_screen = 1080 , name = "Player 1")


# Game loop
running = True
clock = pygame.time.Clock()


while running:

    if key.close():
        running = False

    # Clear the screen
    screen.fill(WHITE)

    # Render the background and blocks
    background.render(screen)
    player.render(screen)

    # Example interaction (move blocks or damage a block)
    
    
    if not player.jump:
        if background.check_down(x_player = player.x , y_player = player.y , deplacement = 1) == 1:
            player.jump = True
            v_ini = 0
            compteur_jump = 0
            dist_theo=0
            dist_real=0
        elif key.up():
            player.jump = True
            v_ini = V0
            compteur_jump = 0
            dist_theo=0
            dist_real=0
    else:
        if background.check_down(x_player = player.x , y_player = player.y , deplacement = 1) == 0:
            player.jump = False
            v_ini = 0
            compteur_jump = 0
            dist_theo=0
            dist_real=0
        if background.check_up(x_player = player.x , y_player = player.y , deplacement = 2) <= 1:
            v_ini = 0
            compteur_jump = 0
            dist_theo=0
            dist_real=0
            

    if key.right() and not key.left():
        player.change_skin("right")
    if key.left() and not key.right():
        player.change_skin("left")
    
    deplacement_down,deplacement_up,deplacement_right,deplacement_left=None,None,None,None
    if player.jump:
        compteur_jump += 1
        dist_theo = (v_ini - g * compteur_jump // 120) * compteur_jump // 60
        depl = dist_theo - dist_real
        dist_real = dist_theo
        if depl > 0:
            if key.right() and not key.left():
                deplacement_up,deplacement_right=background.check_up_right(x_player=player.x,y_player=player.y,deplacement_up=depl,deplacement_right=dx)
                if deplacement_up==0:
                    deplacement_right = background.check_right(x_player = player.x , y_player = player.y , deplacement = dx)
            elif key.left() and not key.right():
                deplacement_up,deplacement_left=background.check_up_left(x_player=player.x,y_player=player.y,deplacement_up=depl,deplacement_left=dx)
                if deplacement_up == 0:
                    deplacement_left = background.check_left(x_player = player.x , y_player = player.y , deplacement = dx)
            else:
                deplacement_up = background.check_up(x_player=player.x,y_player=player.y,deplacement=depl)
        elif depl < 0:
            if key.right() and not key.left():
                deplacement_down,deplacement_right=background.check_down_right(x_player=player.x,y_player=player.y,deplacement_down=-depl,deplacement_right=dx)
            elif key.left() and not key.right():
                deplacement_down,deplacement_left=background.check_down_left(x_player=player.x,y_player=player.y,deplacement_down=-depl,deplacement_left=dx)
            else:
                deplacement_down = background.check_down(x_player=player.x,y_player=player.y,deplacement=-depl)

    else:
        if key.right() and not key.left():
            deplacement_right = background.check_right(x_player = player.x , y_player = player.y , deplacement = dx)
        if key.left() and not key.right():
            deplacement_left = background.check_left(x_player = player.x , y_player = player.y , deplacement = dx)

    if deplacement_down is not None:
        background.down(deplacement_down)
    if deplacement_up is not None:
        background.up(deplacement_up)
    if deplacement_left is not None:
        background.left(deplacement_left)
    if deplacement_right is not None:
        background.right(deplacement_right)
                    

    # Update the screen
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
