from jeu import jeu
from affiche import display_game_state
from classegrille import Grille

# Initialize the game grid
grille = Grille(taille=4, theme="0")

# Run the game and display each game state
for current_grille in jeu():
    display_game_state(current_grille)

print("Game over!")
