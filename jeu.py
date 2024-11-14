import time
import key_handler
from classegrille import Grille

# Initialize the game grid
grille = Grille(theme="0")

def jeu():
    yield grille
    handler = key_handler.KeyHandler()

    try:
        while True:
            # Get the direction from the key handler
            direction = handler.get_direction()

            # Attempt to move based on direction
            moved = False
            if direction == "haut":
                moved = grille.haut()  # Move up
            elif direction == "gauche":
                moved = grille.gauche()  # Move left
            elif direction == "bas":
                moved = grille.bas()  # Move down
            elif direction == "droite":
                moved = grille.droite()  # Move right
            elif direction == "quitter":
                break #On arrête le jeu

            if not moved:
                continue  # Ignore invalid or unsuccessful moves

            # Yield the updated grid after a successful move
            yield grille

            # Check if the game can continue
            if not grille.verif():
                break  # End game if no moves left

            time.sleep(0.05)

    except KeyboardInterrupt:
        pass  # Handle exit gracefully if interrupted
    
    grille.fin_du_jeu()
