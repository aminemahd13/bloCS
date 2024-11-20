import pygame
from classes.class_background import Background
from classes.class_block import DirtBlock, StoneBlock, WoodBlock, BedrockBlock, ObsidianBlock
from classes.class_player import Player
import utils.key_handler as key
from utils.coord_to_screen import screen_to_coord
from screens.menu import display_menu, display_tips
from screens.loading_screen import display_loading_screen


"""
the player inventory is updated when he breaks a block
the function damage_block has been changed to add the 'player' argument !!!!
the player can onlyyy add and destroy blocks around him (i.e 80px around him)

"""











# Pygame initialization
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Colors
WHITE = (255, 255, 255)

# Create the game screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Terraria-like Game Test")

# Initialize the background
background = Background(SCREEN_HEIGHT, SCREEN_WIDTH)

#Create the player
player=Player(height_screen = SCREEN_WIDTH , width_screen = SCREEN_HEIGHT , name = "Player 1")



# Game loop
running = True
clock = pygame.time.Clock()

# Initialize mixer for background music
pygame.mixer.init()

# Display the menu
while True:
    choice = display_menu(screen)
    if choice == "Start Game":
        break
    elif choice == "Tips":
        display_tips(screen)
    elif choice == "Quit":
        pygame.quit()
        exit()

# Display the loading screen
display_loading_screen(screen)

# Play game background music
pygame.mixer.music.load("assets/audio/game.mp3")
pygame.mixer.music.play(-1)  # Loop the music

while running:
    #On capture les touches
    key_close = key.close()
    player.act_touches()
    
    if key_close: #Si on clique sur échap, le jeu se ferme
        running = False
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            player.mining_or_breaking(background = background , event = event)
        elif event.type == player.RESET_MINING_EVENT:
            player.mining = False
            pygame.time.set_timer(player.RESET_MINING_EVENT, 0)  # Stop the timer

    # Clear the screen
    screen.fill(WHITE)

    # Render the background and players
    background.render(screen = screen , player = player) #Affiche le background avec les blocs
    player.render(screen) #Affiche le joueur

    # Draw the inventory
    player.draw_inventory(screen)
    
    #On regarde si le joueur est en plein saut et on actualise sa data
    player.check_if_jumping(background = background)
            

    #Changement du skin
    player.change_skin()
    
    
    #Déplacement du perso
    player.deplacer_perso(background = background)
    
    
    #On garde en mémoire l'état des touches
    player.act_hist_touches()

    # Update the screen
    pygame.display.flip()


    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.mixer.music.stop()
pygame.quit()
