from classes.classetuile import Tuile

def copie_tuile(tuile : Tuile):
    """
    Copie une tuile.
    """
    return Tuile(x_centre = tuile.x , y_centre = tuile.y , valeur = tuile.valeur , taille = tuile.taille)

def copie_ligne(ligne : list) -> list:
    """
    Copie terme à terme la ligne.
    """
    ligne_copy=[]
    for j in range(4):
        ligne_copy.append(copie_tuile(ligne[j]))
    return ligne_copy

def copie_grille(grille: list) -> list:
    """
    Copie terme à terme la grille.
    """
    grille_copy=[]
    for i in range(4):
        grille_copy.append(copie_ligne(grille[i]))
    return grille_copy

def copie_matrice(grille : list) -> list:
    """
    Copie terme à terme la grille.
    """
    grille_copy=[]
    for i in range(4):
        row = []
        for j in range(4):
            row.append(grille[i][j])
        grille_copy.append(row)
    return grille_copy