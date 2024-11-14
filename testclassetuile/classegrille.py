import functions.ajout_aleatoire as ajout_aleatoire
import functions.gauche as gauche
import tkinter as tk

add_random = ajout_aleatoire.add_random
gauche_ligne = gauche.gauche_ligne

def copie(grille: list) -> list:
    """
    Copie terme à terme le tableau.
    """
    return [row[:] for row in grille]

def create_filled_circle(canvas, x, y, radius, couleur):
    # Dessine un cercle plein avec le centre en (x, y) et le rayon spécifié
    canvas.create_oval(x - radius, y - radius, x + radius-1, y + radius-1, fill=couleur, width=0)

def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius, couleur):
    create_filled_circle(canvas, x1+radius, y1+radius, radius, couleur)
    create_filled_circle(canvas, x2-radius, y1+radius, radius, couleur)
    create_filled_circle(canvas, x1+radius, y2-radius, radius, couleur)
    create_filled_circle(canvas, x2-radius, y2-radius, radius, couleur)
    canvas.create_rectangle(x1+radius, y1, x2-radius, y2, fill=couleur, width=0)
    canvas.create_rectangle(x1, y1+radius, x2, y2-radius, fill=couleur, width=0)

def get_couleur(value, dict_couleur):
    if value<=2048:
        return dict_couleur[value]
    else:
        return "#3C3A32"

class Grille:
    def __init__(self, theme: str):
        grille_zero = [[0 for _ in range(4)] for _ in range(4)]
        self.grille = copie(grille_zero)
        self.theme = theme
        self.score = 0
        for _ in range(2):
            self.score = add_random(grille=self.grille, score=self.score)
        # Couleurs pour chaque valeur de tuile
        self.__dict_couleur = {
            0: "#CDC1B4",
            2: "#EEE4DA",
            4: "#EDE0C8",
            8: "#F2B179",
            16: "#F59563",
            32: "#F67C5F",
            64: "#F65E3B",
            128: "#EDCF72",
            256: "#EDCC61",
            512: "#EDC850",
            1024: "#EDC53F",
            2048: "#EDC22E"
        }
        self.__radius = 10
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
    
    def affiche(self):
        self.__canvas.delete("all")
        for i in range(4):
            for j in range(4):
                valeur = self.grille[i][j]
                longueur = len(str(valeur))
                x1, y1 = self.__taille_espace + j * (self.__taille_espace + self.__taille_tuile) , self.__taille_espace + i * (self.__taille_espace + self.__taille_tuile)
                x2, y2 = x1 + self.__taille_tuile, y1 + self.__taille_tuile
                couleur = get_couleur(valeur, self.__dict_couleur)
                create_rounded_rectangle(self.__canvas, x1, y1, x2, y2, self.__radius, couleur)
                if longueur<=2:
                    police = 36
                elif longueur==3:
                    police = 30
                else:
                    police=24
                if valeur != 0:
                    if valeur<=4 :
                        self.__canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=str(valeur), font=("Helvetica", police, "bold"), fill="black")
                    else:
                        self.__canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=str(valeur), font=("Helvetica", police, "bold"), fill="white")
        text_score = "Score : "+str(self.score)
        self.__canvas.create_text(self.__taille_grille//2,self.__taille_grille+50, text=text_score, font=("Helvetica", 24, "bold"), fill="black")
        self.__root.update()
        
    def gauche(self) -> bool:
        changement = False
        new_grille = copie(self.grille)
        for i, row in enumerate(new_grille):
            gauche_ligne(row)
            if row != self.grille[i]:
                changement = True

        if changement:
            self.grille = copie(new_grille)
            self.score = add_random(grille=self.grille, score=self.score)
        return changement

    def _rotation_horaire(self) -> None:
        self.grille = [[self.grille[4 - j - 1][i] for j in range(4)] for i in range(4)]

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
        grille_copy = copie(self.grille)
        original_score = self.score
        for move in [self.droite, self.gauche, self.haut, self.bas]:
            if move():
                self.grille = grille_copy
                self.score = original_score
                return True
        return False
    
    def fin_du_jeu(self) -> None:
        self.__canvas.create_rectangle(0,self.__taille_grille,self.__taille_grille,self.__taille_grille+100, fill="#BBADA0",width=0)
        self.__canvas.create_text(self.__taille_grille//2,self.__taille_grille+30, text="Game over !", font=("Helvetica", 24, "bold"), fill="black")
        self.__canvas.create_text(self.__taille_grille//2,self.__taille_grille+60, text=f"Score final : {self.score}", font=("Helvetica", 24, "bold"), fill="black")
        self.__root.mainloop()