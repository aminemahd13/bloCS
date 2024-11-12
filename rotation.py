def rotation_horaire(matrice):
    n = len(matrice)
    matrice_rotated = [[0] * n for _ in range(n)]  # Crée une matrice vide de même taille
    
    for i in range(n):
        for j in range(n):
            matrice_rotated[j][n - i - 1] = matrice[i][j]
    
    grille = matrice_rotated