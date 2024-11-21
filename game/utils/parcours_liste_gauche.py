from game.utils.copie import copie_ligne_int

def parcours_liste(liste : list):
    """
    Renvoie une liste contenant, pour chaque tuile lors d'un tassement à gauche
    [indice_initial, indice_final, fusion]
    Fusion = 0 si pas de fusion, 1 si la tuile va grossir, 2 si la tuile se fait "absorber"
    """
    #Initialisation de la liste finale
    liste_finale = [None for k in range(4)]
    for j in range(4):
        if liste[j]!=0:
            liste_finale[j]=[j , j , 0]
    
    ligne_copie = copie_ligne_int(liste)
    
    #On tasse à gauche
    for _ in range(3):
        for j in range(1, 4):
            if ligne_copie[j - 1] == 0 and ligne_copie[j]!=0:
                #On déplace la tuile sur la gauche
                ligne_copie[j - 1] = ligne_copie[j]
                ligne_copie[j] = 0
                for tuile in liste_finale:
                    if tuile is not None:
                        if tuile[1]==j:
                            #On change l'indice final de la grille qu'on vient de déplacer
                            tuile[1] = j - 1
    
    #On fusionne
    for j in range(1, 4):
        if ligne_copie[j - 1] == ligne_copie[j]:
            #On fusionne
            ligne_copie[j - 1] = ligne_copie[j - 1] * 2
            ligne_copie[j] = 0
            for tuile in liste_finale:
                if tuile is not None:
                    if tuile[1]==j - 1:
                        #On indique que la tuile devra grossir
                        tuile[2] = 1
                    if tuile[1]==j:
                        #On fait bouger l'indice final de la tuile
                        tuile[1] = j - 1
                        #On indique que la tuile se fait absorber
                        tuile[2] = 2
    
    #On tasse à gauche
    for _ in range(3):
        for j in range(1, 4):
            if ligne_copie[j - 1] == 0 and ligne_copie[j]!=0:
                #On déplace la tuile sur la gauche
                ligne_copie[j - 1] = ligne_copie[j]
                ligne_copie[j] = 0
                for tuile in liste_finale:
                    if tuile is not None:
                        if tuile[1]==j:
                            #On change l'indice final de la grille qu'on vient de déplacer
                            tuile[1] = j - 1
    return liste_finale