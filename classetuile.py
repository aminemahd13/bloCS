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
    def __init__(self, n_ligne, n_colonne, value):
        self.__radius = 10
        self.__taille_tuile = 100
        self.__taille_espace = 10
        self.x = self.__taille_espace + n_colonne*(self.__taille_tuile + self.__taille_espace) + self.__taille_tuile//2
        self.y = self.__taille_espace + n_ligne*(self.__taille_tuile + self.__taille_espace) + self.__taille_tuile//2
        self.value = value
    
    
        