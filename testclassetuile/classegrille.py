import ajout_aleatoire
import gauche
import tkinter as tk
from classetuile import Tuile

add_random = ajout_aleatoire.add_random
gauche_ligne = gauche.gauche_ligne

def copie_ligne(ligne : list) -> list:
    """
    Copie terme à terme la ligne.
    """
    ligne_copy=[]
    for j in range(4):
        ligne_copy.append(Tuile(n_colonne=j,n_ligne=ligne[0].n_ligne,valeur=ligne[j].valeur))
    return ligne_copy

def copie_grille(grille: list) -> list:
    """
    Copie terme à terme le tableau.
    """
    grille_copy=[]
    for i in range(4):
        row=[]
        for j in range(4):
            row.append(Tuile(n_colonne=j,n_ligne=i,valeur=grille[i][j].valeur))
        grille_copy.append(row)
    return grille_copy

class Grille:
    def __init__(self):
        self.__taille_tuile = 100
        self.__taille_espace = 10
        self.__taille_grille = 4 * (self.__taille_tuile + self.__taille_espace) + self.__taille_espace
        # Configuration de la fenêtre principale
        self.__root = tk.Tk()
        self.__root.title("2048")
        self.__root.geometry(f"{self.__taille_grille}x{self.__taille_grille+100}")
        self.__root.config(bg="#BBADA0")
        # Crée un canvas pour dessiner la grille
        self.__canvas = tk.Canvas(self.__root, width=self.__taille_grille, height=self.__taille_grille+100, bg="#BBADA0")
        self.__canvas.pack()
        
        grille_zero = [[Tuile(n_colonne=j, n_ligne=i, valeur=0) for j in range(4)] for i in range(4)]
        self.grille = copie_grille(grille_zero)
        self.score = 0
        for _ in range(2):
            self.score = add_random(grille=self.grille, score=self.score)
        
    
    def affiche(self):
        print("Test")
        self.__canvas.delete("all")
        for i in range(4):
            for j in range(4):
                self.grille[i][j].affiche(self.__canvas)
        text_score = "Score : "+str(self.score)
        self.__canvas.create_text(self.__taille_grille//2,self.__taille_grille+50, text=text_score, font=("Helvetica", 24, "bold"), fill="black")
        self.__root.update()
        
    def gauche(self) -> bool:
        changement = False
        for i in range(4):
            row=copie_ligne(self.grille[i])
            test = gauche_ligne(row)
            changement = changement or test
            if test:
                self.grille[i]=copie_ligne(row)
        if changement:
            self.score = add_random(grille=self.grille, score=self.score)
        return changement

    def _rotation_horaire(self) -> None:
        grille_copy=copie_grille(self.grille)
        for i in range(4):
            for j in range(4):
                self.grille[i][j].valeur = grille_copy[4 - j - 1][i].valeur
        
    def droite(self) -> bool:
        self._rotation_horaire()
        self._rotation_horaire()
        changed = self.gauche()
        self._rotation_horaire()
        self._rotation_horaire()
        return changed

    def haut(self) -> bool:
        self._rotation_horaire()
        self._rotation_horaire()
        self._rotation_horaire()
        changed = self.gauche()
        self._rotation_horaire()
        return changed

    def bas(self) -> bool:
        self._rotation_horaire()
        changed = self.gauche()
        self._rotation_horaire()
        self._rotation_horaire()
        self._rotation_horaire()
        return changed

    def verif(self) -> bool:
        grille_copy = copie_grille(self.grille)
        original_score = self.score
        for move in [self.droite, self.gauche, self.haut, self.bas]:
            if move():
                self.grille = copie_grille(grille_copy)
                self.score = original_score
                return True
        return False
    
    def fin_du_jeu(self) -> None:
        self.__canvas.create_rectangle(0,self.__taille_grille,self.__taille_grille,self.__taille_grille+100, fill="#BBADA0",width=0)
        self.__canvas.create_text(self.__taille_grille//2,self.__taille_grille+30, text="Game over !", font=("Helvetica", 24, "bold"), fill="black")
        self.__canvas.create_text(self.__taille_grille//2,self.__taille_grille+60, text=f"Score final : {self.score}", font=("Helvetica", 24, "bold"), fill="black")
        self.__root.mainloop()