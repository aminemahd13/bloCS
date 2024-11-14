import os
from jeu import jeu
from affiche import affiche
from classegrille import Grille

def reset_screen():
    os.system("cls" if os.name == "nt" else "clear")

grille = Grille(taille=4, theme="0") 

game_state = jeu()
def display_game_state(grille):
    reset_screen()
    # Print the current board and score
    for row in grille.grille:
        print(" ".join(map(str, row)))  # Display each row of the grid
    print(f"Score: {grille.score}")

while True :
    display_game_state(grille)
