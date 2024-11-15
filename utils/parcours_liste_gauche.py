def copie_ligne(ligne : list) -> list:
    """
    Copie terme à terme la ligne.
    """
    ligne_copy=[]
    for j in range(4):
        ligne_copy.append(ligne[j])
    return ligne_copy

def parcours_liste(liste : list):
    taille=4
    liste_finale=[None for k in range(taille)]
    for j in range(taille):
        if liste[j]!=0:
            liste_finale[j]=[j,j,False]
    ligne_copie=copie_ligne(liste)
    
    for _ in range(taille-1):  
        for j in range(1, taille):
            if ligne_copie[j - 1] == 0 and ligne_copie[j]!=0:
                ligne_copie[j - 1] = ligne_copie[j]
                ligne_copie[j] = 0
                for tuile in liste_finale:
                    if tuile !=None:
                        if tuile[1]==j:
                            tuile[1]=j-1
    
    for j in range(1, taille):
        if ligne_copie[j - 1] == ligne_copie[j]:
            ligne_copie[j - 1] = ligne_copie[j - 1] * 2
            ligne_copie[j] = 0
            for tuile in liste_finale:
                if tuile !=None:
                    if tuile[1]==j-1:
                        tuile[2]=True
                    if tuile[1]==j:
                        tuile[1]=j-1
    
    
    for _ in range(taille-1):  
        for j in range(1, taille):
            if ligne_copie[j - 1] == 0 and ligne_copie[j]!=0:
                ligne_copie[j - 1] = ligne_copie[j]
                ligne_copie[j] = 0
                for tuile in liste_finale:
                    if tuile !=None:
                        if tuile[1]==j:
                            tuile[1]=j-1
    return liste_finale