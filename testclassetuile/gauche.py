from classetuile import Tuile

def gauche_ligne(ligne: list) -> None:
    """
    Modifie la liste en fusionnant tout sur la gauche.
    """
    changement = False
    # On rabbat à gauche
    for _ in range(
        4 - 1
    ):  # On réalise l'opération n-1 fois pour tout bien décaler
        for j in range(1, 4):
            if ligne[j - 1].valeur == 0 and ligne[j].valeur!=0:
                changement = True
                ligne[j - 1].valeur = ligne[j].valeur
                ligne[j].valeur = 0
    # On fusionne les chiffres
    for j in range(1, 4):
        if ligne[j - 1].valeur == ligne[j].valeur:
            changement = True
            ligne[j - 1].valeur = ligne[j - 1].valeur * 2
            ligne[j].valeur = 0
    # On rabbat à gauche
    for _ in range(
        4 - 1
    ):  # On réalise l'opération n-1 fois pour tout bien décaler
        for j in range(1, 4):
            if ligne[j - 1].valeur == 0 and ligne[j].valeur!=0:
                changement = True
                ligne[j - 1].valeur = ligne[j].valeur
                ligne[j].valeur = 0
    return changement
