import keyboard

#Dictionnaire contenant les touches associées à telle ou telle direction
direction={"up" : ['w','z','up','space'] , "down" : ['s','down'] , "right" : ['d' , 'right'] , "left" : ['q' , 'a' , 'left'] , "close" : ['esc']}
numbers={ "1":['1'] , "2":['2'] , "3":['3'] , "4":['4'] , "5":['5'] , "6":['6'] , "7":['7'] , "8":['8'] , "9":['9'] , "0":['0']}


def get_number() -> str:
    """
    Renvoie le chiffre que l'utilisateur a tapé
    """
    for i in numbers:
        if keyboard.is_pressed(numbers[i][0]):
            return i
    return -1



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