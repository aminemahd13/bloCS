import keyboard

#Dictionnaire contenant les touches associées à telle ou telle direction
direction={"up" : ['w','z','up'] , "down" : ['s','down'] , "right" : ['d' , 'right'] , "left" : ['q' , 'a' , 'left'] , "close" : ['esc']}

def up() -> bool:
    """
    Renvoie True si l'utilisateur appuie sur une touche
    pour faire tasser la grille en haut, False sinon.
    """
    test = False
    for i in direction["up"]:
        test = test or keyboard.is_pressed(i)
    return test

def down() -> bool:
    """
    Renvoie True si l'utilisateur appuie sur une touche
    pour faire tasser la grille en bas, False sinon.
    """
    test = False
    for i in direction["down"]:
        test = test or keyboard.is_pressed(i)
    return test

def right() -> bool:
    """
    Renvoie True si l'utilisateur appuie sur une touche
    pour faire tasser la grille à droite, False sinon.
    """
    test = False
    for i in direction["right"]:
        test = test or keyboard.is_pressed(i)
    return test

def left() -> bool:
    """
    Renvoie True si l'utilisateur appuie sur une touche
    pour faire tasser la grille à gauche, False sinon.
    """
    test = False
    for i in direction["left"]:
        test = test or keyboard.is_pressed(i)
    return test

def close() -> bool:
    """
    Renvoie True si l'utilisateur appuie sur une touche
    pour faire stopper le jeu, False sinon.
    """
    test = False
    for i in direction["close"]:
        test = test or keyboard.is_pressed(i)
    return test