from utils.jeu import jeu
import time

# Run the game and display each game state
for current_grille in jeu():
    current_grille.affiche()