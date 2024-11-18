from random import randint
from utils.cancel_transition import cancel_transition, creation_hist_touches
import time

def add_random(grille: list, score: int, n_images2 : int, tps : float, canvas : any, root : any) -> None:
    """
    Ajoute, si possible, un nombre aléatoire sur la grille.
    Renvoie le score actualisé.
    """
    hist_touches = creation_hist_touches()
    cancel_animation = False
    liste_zeros = []  # Liste qui contient les coordonnées des cases vides
    for i in range(len(grille)):
        for j in range(len(grille)):
            if grille[i][j].valeur == 0:
                liste_zeros.append((i, j))  # ajoute dans liste_zeros toutes les coordonnées des cases vides

    if len(liste_zeros) > 0:  # on n'effectue le programme que si la grille comporte des cases vides
        case_select = liste_zeros[randint(0, len(liste_zeros) - 1)]  # select une case vide aléatoirement
        (x, y) = case_select
        proba = randint(1, 5)
        new_number = 0
        if proba == 1:
            new_number = 4
        else:
            new_number = 2  # choisis le nombre à ajouter sur la case séléctionnée avec une proba de 1/5 pour 4 et 4/5 pour 2
        grille[x][y].valeur = new_number  # modifie la grille
        score += new_number  # On ajoute ça dans le score
        for image in range(n_images2):
            if not cancel_animation:
                cancel_animation = cancel_animation or cancel_transition(hist_touches)
            if not cancel_animation:
                if image<n_images2//2: #1ère partie de l'animation : on grossit
                    grossissement_police = 2.36 * image / n_images2
                else: #2ème partie de l'animation : on rétressit
                    grossissement_police = 1.36 - 0.36 * (image / n_images2)
                grille[x][y].affiche(canvas, True, grossissement_police)
                root.update() #On actualise la fenêtre graphique
                time.sleep(tps)
    return score
