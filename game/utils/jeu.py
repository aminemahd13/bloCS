import time
import utils.key_handler as key
from game.classes.classegrille import Grille

touche={"haut" : False, "bas" : False, "droite" : False, "gauche" : False}

def jeu(grille : Grille , inventory : dict):
    grille.affiche(inventory) #Affiche la grille

    moved = False
    if key.up():
        if not touche["haut"] and not moved:
            touche["haut"] = True
            moved = grille.haut()  # Move up
    else:
        touche["haut"] = False
         
    if key.left() :
        if not touche["gauche"] and not moved:
            touche["gauche"] = True
            moved = grille.gauche()  # Move left
    else:
        touche["gauche"] = False
          
            
    if key.down():
        if not touche["bas"] and not moved:
            touche["bas"] = True
            moved = grille.bas()  # Move down
    else:
        touche["bas"] = False
            
    if key.right():
        if not touche["droite"] and not moved:
            touche["droite"] = True
            moved = grille.droite()  # Move right
    else:
        touche["droite"]=False
            
    if key.closegame():
        return False
            
    if moved: # Ignore invalid or unsuccessful moves
        # Show the updated grid after a successful move
        grille.affiche(inventory)
        # Check if the game can continue
        if not grille.verif():
            return False  # End game if no moves left
    
    return True
