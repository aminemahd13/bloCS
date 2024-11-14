import tkinter as tk

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

class Tuile:
    def __init__(self, n_ligne, n_colonne, valeur):
        self.n_ligne=n_ligne
        self.n_colonne=n_colonne
        self.__radius = 10
        self.__taille_tuile = 100
        self.__taille_espace = 10
        self.x = self.__taille_espace + n_colonne*(self.__taille_tuile + self.__taille_espace) + self.__taille_tuile//2
        self.y = self.__taille_espace + n_ligne*(self.__taille_tuile + self.__taille_espace) + self.__taille_tuile//2
        self.valeur = valeur
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
        
    def affiche(self, canvas):
        longueur = len(str(self.valeur))
        x1, y1 = self.x - self.__taille_tuile//2 , self.y - self.__taille_tuile//2
        x2, y2 = self.x + self.__taille_tuile//2 , self.y + self.__taille_tuile//2
        couleur = get_couleur(self.valeur, self.__dict_couleur)
        create_rounded_rectangle(canvas, x1, y1, x2, y2, self.__radius, couleur)
        if longueur<=2:
            police = 36
        elif longueur==3:
            police = 30
        else:
            police=24
        if self.valeur != 0:
            if self.valeur<=4 :
                canvas.create_text(self.x, self.y, text=str(self.valeur), font=("Helvetica", police, "bold"), fill="black")
            else:
                canvas.create_text(self.x, self.y, text=str(self.valeur), font=("Helvetica", police, "bold"), fill="white")
        