from input_handlers.key_handler import up, down, right, left, close

def creation_hist_touches() -> dict:
    """
    Renvoie un dicionnaire contenant, à l'état actuel,
    les touches haut, bas, gauche, droite pressées ou non.
    """
    return {"haut" : up() , "bas" : down() , "droite" : right() , "gauche" : left()}

def cancel_transition(hist_touches : dict) -> bool:
    """
    Vérifie si l'utilisateur souhaite ou non faire un autre mouvement,
    ce qui annulerait la transition.
    """
    if not hist_touches["bas"] and down():
        return True
    if not hist_touches["haut"] and up():
        return True
    if not hist_touches["droite"] and right():
        return True
    if not hist_touches["gauche"] and left():
        return True
    if close():
        return True
    
    if hist_touches["bas"] and not down():
        hist_touches["bas"] = False
    if hist_touches["haut"] and not up():
        hist_touches["haut"] = False
    if hist_touches["droite"] and not right():
        hist_touches["droite"] = False
    if hist_touches["gauche"] and not left():
        hist_touches["gauche"] = False
    
    return False