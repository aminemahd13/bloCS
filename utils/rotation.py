from utils.copie import copie_grille, copie_matrice

def rotation_horaire_grille(grille : list) -> list:
        """
        Effectue une rotation horaire de la grille.
        """
        grille_copy = copie_grille(grille)
        for i in range(4):
            for j in range(4):
                #On change uniquement les valeurs !!!
                grille_copy[i][j].valeur = grille[4 - j - 1][i].valeur
        return grille_copy

def rotation_antihoraire_grille(grille : list) -> list:
        """
        Effectue une rotation horaire de la grille.
        """
        grille_copy = copie_grille(grille)
        for i in range(4):
            for j in range(4):
                #On change uniquement les valeurs !!!
                grille_copy[4 - j - 1][i].valeur = grille[i][j].valeur
        return grille_copy

def rotation_double_grille(grille : list) -> list:
        """
        Effectue une rotation horaire de la grille.
        """
        grille_copy = copie_grille(grille)
        for i in range(4):
            for j in range(4):
                #On change uniquement les valeurs !!!
                grille_copy[4 - i - 1][4 - j - 1].valeur = grille[i][j].valeur
        return grille_copy

def rotation_horaire_matrice(grille : list) -> list:
        """
        Effectue une rotation horaire de la grille.
        """
        grille_copy = copie_matrice(grille)
        for i in range(4):
            for j in range(4):
                #On change uniquement les valeurs !!!
                grille_copy[i][j] = grille[4 - j - 1][i]
        return grille_copy

def rotation_antihoraire_matrice(grille : list) -> list:
        """
        Effectue une rotation horaire de la grille.
        """
        grille_copy = copie_matrice(grille)
        for i in range(4):
            for j in range(4):
                #On change uniquement les valeurs !!!
                grille_copy[4 - j - 1][i] = grille[i][j]
        return grille_copy

def rotation_double_matrice(grille : list) -> list:
        """
        Effectue une rotation horaire de la grille.
        """
        grille_copy = copie_matrice(grille)
        for i in range(4):
            for j in range(4):
                #On change uniquement les valeurs !!!
                grille_copy[4 - i - 1][4 - j - 1] = grille[i][j]
        return grille_copy