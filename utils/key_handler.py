import pygame

# Initialize pygame
pygame.init()

# Dictionnaire contenant les touches associées à telle ou telle direction
direction = {
    "up": [pygame.K_w, pygame.K_z, pygame.K_UP, pygame.K_SPACE],
    "down": [pygame.K_s, pygame.K_DOWN],
    "right": [pygame.K_d, pygame.K_RIGHT],
    "left": [pygame.K_q, pygame.K_a, pygame.K_LEFT],
    "close": [pygame.K_ESCAPE],
    "h" : [pygame.K_h]
}
numbers = {
    "1": [pygame.K_1],
    "2": [pygame.K_2],
    "3": [pygame.K_3],
    "4": [pygame.K_4],
    "5": [pygame.K_5],
    "6": [pygame.K_6],
    "7": [pygame.K_7],
    "8": [pygame.K_8],
    "9": [pygame.K_9],
    "0": [pygame.K_0]
}

def get_number() -> str:
    """
    Renvoie le chiffre que l'utilisateur a tapé
    """
    keys = pygame.key.get_pressed()
    for num, key_list in numbers.items():
        if any(keys[key] for key in key_list):
            return num
    return -1

def up() -> bool:
    """
    Renvoie True si l'utilisateur appuie sur une touche
    pour faire tasser la grille en haut, False sinon.
    """
    keys = pygame.key.get_pressed()
    return any(keys[key] for key in direction["up"])

def down() -> bool:
    """
    Renvoie True si l'utilisateur appuie sur une touche
    pour faire tasser la grille en bas, False sinon.
    """
    keys = pygame.key.get_pressed()
    return any(keys[key] for key in direction["down"])

def right() -> bool:
    """
    Renvoie True si l'utilisateur appuie sur une touche
    pour faire tasser la grille à droite, False sinon.
    """
    keys = pygame.key.get_pressed()
    return any(keys[key] for key in direction["right"])

def left() -> bool:
    """
    Renvoie True si l'utilisateur appuie sur une touche
    pour faire tasser la grille à gauche, False sinon.
    """
    keys = pygame.key.get_pressed()
    return any(keys[key] for key in direction["left"])

def close() -> bool:
    """
    Renvoie True si l'utilisateur appuie sur une touche
    pour faire stopper le jeu, False sinon.
    """
    keys = pygame.key.get_pressed()
    return any(keys[key] for key in direction["close"])

def changemod() -> bool:
    """
    Renvoie True si l'utilisateur appuie sur une touche
    pour faire chnger le fond, False sinon.
    """
    keys = pygame.key.get_pressed()
    return any(keys[key] for key in direction["h"])