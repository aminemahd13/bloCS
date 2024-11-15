import tkinter as tk

def create_filled_circle(canvas, x : int, y : int, radius : int, couleur : str) -> None:
    """
    Dessine un cercle plein avec le centre en (x, y) et le rayon spécifié
    sur le canvas, de la couleur spécifiée.
    """
    canvas.create_oval(x - radius , y - radius , x + radius - 1 , y + radius - 1 , fill = couleur , width = 0)

def create_rounded_rectangle(canvas, x1 : int, y1 : int, x2 : int, y2 : int, radius : int, couleur : str) -> None:
    """
    Dessine un rectangle arrondi avec le coin
    haut-gauche (x1,y1) et le coin bas-droit (x2,y2)
    sur le canvas, de la couleur spécifiée.
    """
    create_filled_circle(canvas, x1+radius, y1+radius, radius, couleur)
    create_filled_circle(canvas, x2-radius, y1+radius, radius, couleur)
    create_filled_circle(canvas, x1+radius, y2-radius, radius, couleur)
    create_filled_circle(canvas, x2-radius, y2-radius, radius, couleur)
    canvas.create_rectangle(x1+radius, y1, x2-radius, y2, fill=couleur, width=0)
    canvas.create_rectangle(x1, y1+radius, x2, y2-radius, fill=couleur, width=0)

def get_couleur(value : int, dict_couleur : dict) -> str:
    """
    Renvoie la couleur associée à la valeur.
    """
    if value<=2048:
        return dict_couleur[value]
    else:
        return "#3C3A32"

class Tuile:
    def __init__(self, x_centre : int, y_centre : int, valeur : int, taille : int = 100):
        self.__radius = 10 #Rayon de courbure des coins
        self.taille = taille
        self.x = x_centre
        self.y = y_centre
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
        
    def affiche(self, canvas, chiffre : bool, grossissement = 1) -> None:
        """
        Affiche la tuile à ses coordonnées.
        """
        longueur = len(str(self.valeur))
        #Coins haut-gauche puis bas-droit
        x1, y1 = self.x - self.taille//2 , self.y - self.taille//2
        x2, y2 = self.x + self.taille//2 , self.y + self.taille//2
        couleur = get_couleur(self.valeur, self.__dict_couleur) #Couleur de la valeur
        create_rounded_rectangle(canvas, x1, y1, x2, y2, self.__radius, couleur)
        if chiffre:
            if longueur<=2:
                police = round(36 * grossissement)
            elif longueur==3:
                police = round(30 * grossissement)
            else:
                police = round(24 * grossissement)
            if self.valeur != 0:
                #On affiche le chiffre dans la case
                if self.valeur<=4 :
                    canvas.create_text(self.x, self.y, text=str(self.valeur), font=("Helvetica", police, "bold"), fill="black")
                else:
                    canvas.create_text(self.x, self.y, text=str(self.valeur), font=("Helvetica", police, "bold"), fill="white")
        