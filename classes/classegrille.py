import utils.ajout_aleatoire as ajout_aleatoire
import utils.gauche as gauche
from classes.classetuile import Tuile
import tkinter as tk

add_random = ajout_aleatoire.add_random
gauche_ligne = gauche.gauche_ligne

def copie_tuile(tuile : Tuile):
    return Tuile(x_centre = tuile.x , y_centre = tuile.y , valeur = tuile.valeur , taille = tuile.taille)

def copie_ligne(ligne : list) -> list:
    """
    Copie terme à terme la ligne.
    """
    ligne_copy=[]
    for j in range(4):
        ligne_copy.append(copie_tuile(ligne[j]))
    return ligne_copy

def copie_grille(grille: list) -> list:
    """
    Copie terme à terme la grille.
    """
    grille_copy=[]
    for i in range(4):
        grille_copy.append(copie_ligne(grille[i]))
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
        
        #Initialisation de la grille
        grille_zero = [[Tuile(
            x_centre = self.__taille_espace + j * (self.__taille_tuile + self.__taille_espace) + self.__taille_tuile//2, #Coordonnée x du centre de la tuile
            y_centre = self.__taille_espace + i * (self.__taille_tuile + self.__taille_espace) + self.__taille_tuile//2, #Coordonnée y du centre de la tuile
            valeur=0
            ) for j in range(4)] for i in range(4)]
        self.grille = copie_grille(grille_zero) #On copie pour éviter tout bug (svp)
        self.score = 0 #On initialise le score
        for _ in range(2):
            #On ajoute 2 tuiles au hasard
            self.score = add_random(grille =self.grille, score = self.score)
        
    
    def affiche(self) -> None:
        """
        Affiche l'entièreté de la grille
        dans son état actuel avec le score.
        """
        self.__canvas.delete("all") #On efface tout
        for i in range(4):
            for j in range(4):
                self.grille[i][j].affiche(self.__canvas) #On affiche tuile par tuile
        #On affiche le score
        text_score = "Score : "+str(self.score)
        self.__canvas.create_text(
            self.__taille_grille//2, #Coordonnée x
            self.__taille_grille + 50, #Coordonnée y
            text = text_score,
            font = ("Helvetica", 24, "bold"),
            fill = "black"
            )
        self.__root.update() #On actualise la fenêtre graphique
        
    def gauche(self) -> bool:
        """
        Tasse la grille sur la gauche et renvoie
        True or False si la grille a changée ou non.
        """
        changement = False
        for i in range(4):
            row = copie_ligne(self.grille[i]) #On crée une copie de chaque ligne
            test = gauche_ligne(row) #On tasse la ligne à gauche et on vérifie s'il y a changement surla ligne
            changement = changement or test #Variable qui indique s'il y a au moins 1 changement sur la grille
            if test:
                self.grille[i] = copie_ligne(row) #On actualise la ligne seulement en cas de changement
                
        if changement:
            #Si la grille a bougée, on ajoute 1 case et on actualise le score
            self.score = add_random(grille = self.grille, score = self.score)
        
        return changement

    def _rotation_horaire(self) -> None:
        """
        Effectue une rotation horaire de la grille.
        """
        grille_copy = copie_grille(self.grille)
        for i in range(4):
            for j in range(4):
                #On change uniquement les valeurs !!!
                self.grille[i][j].valeur = grille_copy[4 - j - 1][i].valeur
        
    def droite(self) -> bool:
        """
        Tasse la grille sur la droite et renvoie
        True or False si la grille a changée ou non.
        """
        self._rotation_horaire()
        self._rotation_horaire()
        changed = self.gauche()
        self._rotation_horaire()
        self._rotation_horaire()
        return changed

    def haut(self) -> bool:
        """
        Tasse la grille sur le haut et renvoie
        True or False si la grille a changée ou non.
        """
        self._rotation_horaire()
        self._rotation_horaire()
        self._rotation_horaire()
        changed = self.gauche()
        self._rotation_horaire()
        return changed

    def bas(self) -> bool:
        """
        Tasse la grille sur le bas et renvoie
        True or False si la grille a changée ou non.
        """
        self._rotation_horaire()
        changed = self.gauche()
        self._rotation_horaire()
        self._rotation_horaire()
        self._rotation_horaire()
        return changed

    def verif(self) -> bool:
        """
        Vérifie s'il est possible d'effectuer un mouvement.
        Renvoie True or False
        """
        grille_copy = copie_grille(self.grille)
        original_score = self.score
        for move in [self.droite, self.gauche, self.haut, self.bas]:
            if move():
                #Si un mouvement est possible, on remet la grille et le score d'origine
                #Rem : pas la peine d'actualiser la grille si move()=False
                self.grille = copie_grille(grille_copy)
                self.score = original_score
                return True
        return False
    
    def fin_du_jeu(self) -> None:
        """
        Ferme le jeu.
        """
        self.__canvas.create_rectangle(0,self.__taille_grille,self.__taille_grille,self.__taille_grille+100, fill="#BBADA0",width=0)
        self.__canvas.create_text(self.__taille_grille//2,self.__taille_grille+30, text="Game over !", font=("Helvetica", 24, "bold"), fill="black")
        self.__canvas.create_text(self.__taille_grille//2,self.__taille_grille+60, text=f"Score final : {self.score}", font=("Helvetica", 24, "bold"), fill="black")
        self.__root.mainloop() #On laisse la fenêtre ouverte