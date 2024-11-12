def gauche_ligne(ligne : list) -> None :
    """
    Modifie la liste en fusionnant tout sur la gauche.
    """
    #On rabbat à gauche
    for i in range(len(ligne) - 1) : #On réalise l'opération n-1 fois pour tout bien décaler
        for j in range(1 , len(ligne)) :
            if ligne[j - 1] == 0:
                ligne[j - 1] = ligne[j]
                ligne[j] = 0
    #On fusionne les chiffres
    for j in range(1 , len(ligne)) : 
        if ligne[j - 1] == ligne[j] :
            ligne[j - 1] = ligne[j-1]*2
            ligne[j] = 0
    #On rabbat à gauche
    for i in range(len(ligne) - 1) : #On réalise l'opération n-1 fois pour tout bien décaler
        for j in range(1 , len(ligne)) : 
            if ligne[j - 1] == 0:
                ligne[j - 1] = ligne[j]
                ligne[j] = 0