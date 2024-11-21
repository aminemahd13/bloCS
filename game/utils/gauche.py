from game.utils.copie import copie_ligne

def gauche_ligne(ligne: list) -> bool:
    """
    Modifie la liste en fusionnant tout sur la gauche.
    Renvoie True or False s'il y a un changement ou non.
    """
    changement = False
    # On rabbat à gauche
    for _ in range(3):  # On réalise l'opération n-1 fois pour tout bien décaler
        for j in range(1, 4):
            if ligne[j - 1].valeur == 0 and ligne[j].valeur!=0:
                changement = True
                ligne[j - 1].valeur = ligne[j].valeur
                ligne[j].valeur = 0
    # On fusionne les chiffres
    for j in range(1, 4):
        if ligne[j - 1].valeur == ligne[j].valeur and ligne[j].valeur!=0:
            changement = True
            ligne[j - 1].valeur = ligne[j - 1].valeur * 2
            ligne[j].valeur = 0
    # On rabbat à gauche
    for _ in range(3):  # On réalise l'opération n-1 fois pour tout bien décaler
        for j in range(1, 4):
            if ligne[j - 1].valeur == 0 and ligne[j].valeur!=0:
                changement = True
                ligne[j - 1].valeur = ligne[j].valeur
                ligne[j].valeur = 0
    return changement

def gauche_grille(grille : list) -> tuple:
    """
    Tasse la grille sur la gauche et renvoie
    True or False si la grille a changée ou non
    et la nouvelle grille.
    """
    changement = False
    new_grille=[]
    for i in range(4):
        row = copie_ligne(grille[i]) #On crée une copie de chaque ligne
        test = gauche_ligne(row) #On tasse la ligne à gauche et on vérifie s'il y a changement surla ligne
        changement = changement or test #Variable qui indique s'il y a au moins 1 changement sur la grille
        new_grille.append(copie_ligne(row)) #On actualise la ligne
        
    return changement , new_grille