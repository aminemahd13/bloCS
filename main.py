import pygame
from game.classes.class_background import Background
from game.classes.class_block import DirtBlock, StoneBlock, WoodBlock, BedrockBlock
from game.classes.class_player import Player

# Pygame initialization
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Colors
WHITE = (255, 255, 255)

# Create the game screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Terraria")

# Initialize the background
background = Background(SCREEN_HEIGHT, SCREEN_WIDTH)

# Add some blocks to the background
background.add_block(DirtBlock(100, 200))
background.add_block(StoneBlock(200, 200))
background.add_block(WoodBlock(300, 200))
background.add_block(BedrockBlock(400, 200))

#Create the player
player=Player(height_screen = 1920 , width_screen = 1080 , name = "Player 1")


# Game loop
running = True
clock = pygame.time.Clock()



while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(WHITE)

    # Render the background and blocks
    background.render(screen)
    player.render(screen)

    # Example interaction (move blocks or damage a block)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        background.right(5)
        player.change_skin("right")
    if keys[pygame.K_LEFT]:
        background.left(5)
        player.change_skin("left")
    if keys[pygame.K_DOWN]:
        background.down(5)
    if keys[pygame.K_UP]:
        background.up(5)
        player.jump = True
        player.change_skin("right")
    else:
        player.jump=False
    
    #modifier ça pour que le joueur mine avec la souris si on veut pas utiliser les touches
    if keys[pygame.K_a]:
        player.mining = True
        if keys[pygame.K_RIGHT]:
            player.change_skin("right")
        elif keys[pygame.K_LEFT]:
            player.change_skin("left")
        else: 
            player.change_skin(player.direction)
    else: 
        player.mining = False
        
        

    # Simulate damaging a block at (150, 200)
    if keys[pygame.K_SPACE]:
        if background.damage_block(150, 200, 10):
            print("Block destroyed at (150, 200)!")

    # Update the screen
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
