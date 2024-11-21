from random import randint

def add_random_tuile(grille: list, score: int , valeur : int) -> None:
    """
    Ajoute, si possible, un nombre aléatoire sur la grille.
    Renvoie le score actualisé.
    """
    liste_zeros = []  # Liste qui contient les coordonnées des cases vides
    for i in range(len(grille)):
        for j in range(len(grille)):
            if grille[i][j].valeur == 0:
                liste_zeros.append((i, j))  # ajoute dans liste_zeros toutes les coordonnées des cases vides

    if len(liste_zeros) > 0:  # on n'effectue le programme que si la grille comporte des cases vides
        case_select = liste_zeros[randint(0, len(liste_zeros) - 1)]  # select une case vide aléatoirement
        (x, y) = case_select
        grille[x][y].valeur = valeur  # modifie la grille
        score += valeur  # On ajoute ça dans le score
    return score
