import classegrille
import time
import KeyHandler
import os
import threading

grille = classegrille.Grille(taille=4, theme="0")


def reset_screen():
    os.system("cls" if os.name == "nt" else "clear")


reset_screen()
grille.affiche()
print(f"Score : {grille.score}")


handler = KeyHandler.KeyHandler()

try:
    while True:
        direction = handler.get_direction()

        if direction == "haut":  # Si on appuie sur z
            if (
                grille.haut()
            ):  # Si on peut tasser en haut (dans ce cas, ça tasse automatiquement)
                reset_screen()
                grille.affiche()  # On affiche la grille et le score
                print(f"Score : {grille.score}")
                if not (
                    grille.verif()
                ):  # Si plus aucun mouvement est possible on arrête
                    break
            else:
                print("Mouvement impossible !")

        elif direction == "gauche":  # Si on appuie sur q
            if (
                grille.gauche()
            ):  # Si on peut tasser à gauche (dans ce cas, ça tasse automatiquement)
                reset_screen()
                grille.affiche()  # On affiche la grille et le score
                print(f"Score : {grille.score}")
                if not (grille.verif()):
                    break
            else:
                print("Mouvement impossible !")

        elif direction == "bas":  # Si on appuie sur s
            if (
                grille.bas()
            ):  # Si on peut tasser en bas (dans ce cas, ça tasse automatiquement)
                reset_screen()
                grille.affiche()
                print(f"Score : {grille.score}")
                if not (grille.verif()):
                    break
            else:
                print("Mouvement impossible !")

        elif direction == "droite":  # Si on appuie sur d
            if (
                grille.droite()
            ):  # Si on peut tasser à droite (dans ce cas, ça tasse automatiquement)
                reset_screen()
                grille.affiche()
                print(f"Score : {grille.score}")
                if not (grille.verif()):
                    break
            else:
                print("Mouvement impossible !")

        time.sleep(0.05)

except KeyboardInterrupt:
    print("Programme arrete.")

for i in range(4):
    print(" ")

print(f"Perdu ! Score final : {grille.score}")
