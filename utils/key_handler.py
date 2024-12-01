import pygame

pygame.init()

# Dictionnaire contenant les touches associées à telle ou telle direction
direction = {
    "close": [pygame.K_ESCAPE]
}

def close() -> bool:
    """
    Renvoie True si l'utilisateur appuie sur une touche
    pour faire stopper le jeu, False sinon.
    """
    keys = pygame.key.get_pressed()
    return any(keys[key] for key in direction["close"])