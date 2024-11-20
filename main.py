import pygame
from classes.class_background import Background
from classes.class_block import DirtBlock, StoneBlock, WoodBlock, BedrockBlock, ObsidianBlock
from classes.class_player import Player
import utils.key_handler as key
from utils.coord_to_screen import screen_to_coord
from classes.class_background import draw_inventory

"""
the player inventory is updated when he breaks a block
the function damage_block has been changed to add the 'player' argument !!!!
the player can onlyyy add and destroy blocks around him (i.e 80px around him)

"""









#Variable qui sauvegarde si l'utilisateur touchait les touces droites ou gauche à la frame d'avant
hist_touches = {"right" : key.right() , "left" : key.left()}

# Pygame initialization
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
#Paramètres à ne pas changer !
V0 = 551 #Vitesse initiale lors d'un saut
g = round(V0**2 / (2 * 2.3 * 40)) #Gravité, pour sauter d'une hauteur max de 2.3 blocs
#Paramètres
dx = 6 #Déplacement en px sur les côtés à chaque mouvement
compteur_jump = 0 #Lorsqu'un saut ou une chute a lieu, ce compteur augmente de 1 à chaque frame
dist_theo = 0 #Distance théorique (algébrique, en hauteur) par rapport à l'origine du saut lors d'un saut ou d'une chute
dist_real = 0 #Distance réelle (algébrique, en hauteur) par rapport à l'origine du saut lors d'un saut ou d'une chute


# Colors
WHITE = (255, 255, 255)

# Create the game screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Terraria-like Game Test")

# Initialize the background
background = Background(SCREEN_HEIGHT, SCREEN_WIDTH)

#Create the player
player=Player(height_screen = SCREEN_WIDTH , width_screen = SCREEN_HEIGHT , name = "Player 1")

# Define a custom event for resetting the mining state
RESET_MINING_EVENT = pygame.USEREVENT + 1


selected_block = 1
block_types = ["Dirt", "Stone", "Obsidian", "Wood", "Bedrock"]

# Game loop
running = True
clock = pygame.time.Clock()


while running:
    #On capture les touches
    key_get_number = key.get_number()
    key_up = key.up()
    key_down = key.down()
    key_left = key.left()
    key_right = key.right()
    key_close = key.close()
    
    if key_get_number != -1: #Si on clique sur un chiffre correct pour sélectionner un bloc
        selected_block = int(key_get_number) #On change la sélection
    if key_close: #Si on clique sur échap, le jeu se ferme
        running = False
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x_screen, y_screen = pygame.mouse.get_pos() #Position du click sur l'écran
            #On converti ces coordonnées en coordonnées relatives au background (en px)
            x , y = screen_to_coord(x_screen = x_screen , y_screen = y_screen , player = player)
            if player.x_left() - 80 <= x <= player.x_right() + 80 and player.y_up() - 80 <= y <= player.y_down() + 80:
                #Si on est dans une fenêtre de 2 blocs sur les côtés
                if event.button == 1:  # Left click to place a block
                    selected_block_type = block_types[selected_block - 1] #Type de bloc sélectionné
                    if player.inventory[selected_block_type] > 0: #Si on en a dans notre inventaire
                        new_block = eval(f"{selected_block_type}Block(x = x , y = y)") #Création de l'objet block
                        if background.add_block(new_block): #Si le bloc a été placé
                            player.remove_inventory(selected_block_type) #On l'enlève de l'inventaire
                elif event.button == 3:  # Right click to remove a block
                    background.damage_block(x = x, y = y, damage = 100, player = player) # Remove 100 hp from the block
                    #Remarque : met automatiquement le bloc dans l'inventaire du joueur s'il est détruit
                    player.mining = True
                    pygame.time.set_timer(RESET_MINING_EVENT, 350)  # Set a timer for 1 second
        elif event.type == RESET_MINING_EVENT:
            player.mining = False
            pygame.time.set_timer(RESET_MINING_EVENT, 0)  # Stop the timer

    # Clear the screen
    screen.fill(WHITE)

    # Render the background and players
    background.render(screen = screen , player = player) #Affiche le background avec les blocs
    player.render(screen) #Affiche le joueur

    # Draw the inventory
    draw_inventory(screen, player, selected_block)
    
    #On regarde si le joueur est en plein saut
    
    reinitialisation_saut = False #Variable servant à réinitialiser les variables de saut
    
    if not player.jump: #Si le joueur n'est pas en plein saut
        #On vérifie qu'il y a bien qqlq chose en dessous de lui, sinon il chute
        if background.check_down(player = player,
                                 deplacement = 1 #On regarde le déplacement possible pour un déplacement "élémentaire"
                                 ) == 1:
            player.jump = True #Le joueur chute
            #On initialise les paramètres de chute à 0
            v_ini = 0 #Vitesse initiale de la chute
            reinitialisation_saut = True
        
        #S'il y a un bloc sous ses pieds, on regarde si le joueur veut sauter
        elif key_up:
            if background.check_up(player = player,
                                    deplacement = 1 #On regarde le déplacement possible pour un déplacement "élémentaire"
                                    ) == 1:
                player.jump = True #Le joueur saute
                v_ini = V0 #La vitesse initiale cette fois vaut V0
                reinitialisation_saut = True
    
    
    else: #Si le joueur est déjà en plein saut
        if (key_right and not key_left) or (not hist_touches["right"] and key_right):
            #Si le joueur veut aller à droite
            #Soit il appuie à droite et pas à gauche, soit il appuyait pas à droite la frame d'avant mais maintenant oui
            if background.check_down_right(player = player,
                                           deplacement_down = 1, #On regarde le déplacement possible pour un déplacement "élémentaire"
                                           deplacement_right = 1
                                           )[0] == 0:
                #S'il y a quelque chose sous ses pieds, dès qu'il veut aller en bas à droite, le joueur arrête sa chute
                player.jump = False
                v_ini = 0
                reinitialisation_saut = True
        elif (key_left and not key_right) or (not hist_touches["left"] and key_left):
            #Si le joueur veut aller à gauche
            #Soit il appuie à gauche et pas à droite, soit il appuyait pas à gauche la frame d'avant mais maintenant oui
            if background.check_down_left(player = player,
                                          deplacement_down = 1, #On regarde le déplacement possible pour un déplacement "élémentaire"
                                          deplacement_left = 1
                                          )[0] == 0:
                #S'il y a quelque chose sous ses pieds, dès qu'il veut aller en bas à gauche, le joueur arrête sa chute
                player.jump = False
                v_ini = 0
                reinitialisation_saut = True
        else:
            #S'il n'y a pas de direction particulière (gauche ou droite)
            if background.check_down(player = player,
                                     deplacement = 1 #On regarde le déplacement possible pour un déplacement "élémentaire"
                                     ) == 0:
                #S'il y a qqlq chose en dessous de lui, la chute s'arrête
                player.jump = False
                v_ini = 0
                reinitialisation_saut = True
        if background.check_up(player = player,
                               deplacement = 2 #On regarde le déplacement possible pour un déplacement "élémentaire"
                               ) <= 1:
            #S'il y a un bloc au dessus de lui, la chute ne s'arrête pas mais la vitesse se réinitialise
            v_ini = 0
            reinitialisation_saut = True

    if reinitialisation_saut:
        compteur_jump = 0
        dist_real = 0
        dist_theo = 0
            



    #Changement du skin
    
    moving = False
    if (key_right and not key_left) or (not hist_touches["right"] and key_right):
        #Si le joueur veut aller à droite
        #Soit il appuie à droite et pas à gauche, soit il appuyait pas à droite la frame d'avant mais maintenant oui
        player.direction = "right" #On force la direction du skin
        moving = True #On indique que le skin est en mouvement
    elif (key_left and not key_right) or ((not hist_touches["left"] and key_left)):
        #Si le joueur veut aller à gauche
        #Soit il appuie à gauche et pas à droite, soit il appuyait pas à gauche la frame d'avant mais maintenant oui
        player.direction = "left" #On force la direction du skin
        moving = True #On indique que le skin est en mouvement
    else:
        #Pas de direction imposée : on n'impose pas le skin
        moving = False #On ne fait pas l'animation de marche
    player.change_skin(moving)
    

    
    #Calcul du déplacement effectué
    
    deplacement_down , deplacement_up , deplacement_right , deplacement_left = None , None , None , None
    if player.jump: #Si le joueur est en plein saut
        #On calcule la nouvelle distance théorique
        compteur_jump += 1
        dist_theo = (v_ini - g * compteur_jump // 120) * compteur_jump // 60
        #Déplacement à effectuer
        depl = dist_theo - dist_real
        dist_real = dist_theo #On actualise la vraie distance
        #Remarque : s'il y a un mur en haut ou en bas, le personnage n vas pas bouger verticalement de depl
        #Cependant, à la frame d'après, le jeu va détecter s'il est contre ce mur, et la chute va stopper
        if depl > 0: #Si on monte
            if (key_right and not key_left) or (not hist_touches["right"] and key_right):
                #Si on va à droite
                #On calcule les déplacements qu'on va effectivement réaliser dans les deux directions
                deplacement_up , deplacement_right = background.check_up_right(player = player,
                                                                               deplacement_up = depl,
                                                                               deplacement_right = dx)
            elif (key_left and not key_right) or ((not hist_touches["left"] and key_left)):
                #Si on va à gauche
                #On calcule les déplacements qu'on va effectivement réaliser dans les deux directions
                deplacement_up , deplacement_left = background.check_up_left(player = player,
                                                                             deplacement_up = depl,
                                                                             deplacement_left = dx)
            else:
                #Si on ne bouge pas horizontalement, on monte simplement
                deplacement_up = background.check_up(player = player,
                                                     deplacement = depl)
        
        elif depl < 0: #Si on descend
            if (key_right and not key_left) or (not hist_touches["right"] and key_right):
                #Si on va à droite
                #On calcule les déplacements qu'on va effectivement réaliser dans les deux directions
                deplacement_down , deplacement_right = background.check_down_right(player = player,
                                                                                   deplacement_down = -depl,
                                                                                   deplacement_right = dx)
            elif (key_left and not key_right) or ((not hist_touches["left"] and key_left)):
                #Si on va à gauche
                #On calcule les déplacements qu'on va effectivement réaliser dans les deux directions
                deplacement_down , deplacement_left = background.check_down_left(player = player,
                                                                                 deplacement_down = -depl,
                                                                                 deplacement_left = dx)
            else:
                #Si on ne bouge pas horizontalement, on monte simplement
                deplacement_down = background.check_down(player = player,
                                                         deplacement = -depl)
                
        else: #Si on ne bouge pas verticalement
            if (key_right and not key_left) or (not hist_touches["right"] and key_right):
                #Si on va à droite
                #On calcule le déplacement qu'on va effectivement réaliser dans la direction
                deplacement_right = background.check_right(player = player,
                                                           deplacement = dx)
            elif (key_left and not key_right) or (not hist_touches["left"] and key_left):
                #Si on va à gauche
                #On calcule le déplacement qu'on va effectivement réaliser dans la direction
                deplacement_left=background.check_left(player = player,
                                                       deplacement = dx)


    else: #Si on est pas en plein saut
        if (key_right and not key_left) or (not hist_touches["right"] and key_right):
            #Si on va à droite
            #On calcule le déplacement qu'on va effectivement réaliser dans la direction
            deplacement_right = background.check_right(player = player,
                                                       deplacement = dx)
        if (key_left and not key_right) or (not hist_touches["left"] and key_left):
            #Si on va à gauche
            #On calcule le déplacement qu'on va effectivement réaliser dans la direction
            deplacement_left = background.check_left(player = player,
                                                     deplacement = dx)

    
    
    
    #On effectue les éventuels déplacements
    
    if deplacement_down is not None:
        player.y += deplacement_down
    if deplacement_up is not None:
        player.y -= deplacement_up
    if deplacement_left is not None:
        player.x -= deplacement_left
    if deplacement_right is not None:
        player.x += deplacement_right
    
    
    #On garde en mémoire l'état des touches
    hist_touches["left"] = key_left
    hist_touches["right"] = key_right

    # Update the screen
    pygame.display.flip()


    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
