import time
import key_handler
import os
from classegrille import Grille

# Initialize the game grid
grille = Grille(taille=4, theme="0")

def reset_screen():
    os.system("cls" if os.name == "nt" else "clear")

def get_game_state(grille):
    return [grille.grille, grille.score]  # Return as a list

def display_game_state(grille):
    reset_screen()
    # Print the current board and score
    for row in grille.grille:
        print(" ".join(map(str, row)))  # Display each row of the grid
    print(f"Score: {grille.score}")

def jeu():
    handler = key_handler.KeyHandler()

    try:
        while True:
            # Get the direction from the key handler
            direction = handler.get_direction()

            # Attempt to move based on direction
            if direction == "haut" and grille.haut():
                pass  # Move up
            elif direction == "gauche" and grille.gauche():
                pass  # Move left
            elif direction == "bas" and grille.bas():
                pass  # Move down
            elif direction == "droite" and grille.droite():
                pass  # Move right
            else:
                continue  # Ignore invalid moves or unsuccessful moves

            # Check if the game can continue
            if not grille.verif():
                break  # End game if no moves left

            time.sleep(0.05)

    except KeyboardInterrupt:
        pass  # Handle exit gracefully if interrupted

    # Return the final game state and score as a list
    return get_game_state(grille)

