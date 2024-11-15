import utils.ajout_aleatoire as ajout_aleatoire
import utils.gauche as gauche
from utils.parcours_liste_gauche import parcours_liste
from utils.parcours import parcours
from classes.nv_classetuile import Tuile
import tkinter as tk
import time

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

def copie_matrice(grille : list) -> list:
    """
    Copie terme à terme la grille.
    """
    grille_copy=[]
    for i in range(4):
        row = []
        for j in range(4):
            row.append(grille[i][j])
        grille_copy.append(row)
    return grille_copy

def gauche_grille(grille : list) -> tuple:
    """
    Tasse la grille sur la gauche et renvoie
    True or False si la grille a changée ou non
    et la nouvelle grille.
    """
    changement = False
    new_grille=[]
    for i in range(4):
        row = copie_ligne(grille[i]) #On crée une copie de chaque ligne
        test = gauche_ligne(row) #On tasse la ligne à gauche et on vérifie s'il y a changement surla ligne
        changement = changement or test #Variable qui indique s'il y a au moins 1 changement sur la grille
        new_grille.append(copie_ligne(row)) #On actualise la ligne
        
    return changement , new_grille

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


class Grille:
    def __init__(self):
        self.n_images = 30
        self.tps1 = 0.007
        self.tps2 = 0.002
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
        self.__grille_zero = [[Tuile(
            x_centre = self.__taille_espace + j * (self.__taille_tuile + self.__taille_espace) + self.__taille_tuile//2, #Coordonnée x du centre de la tuile
            y_centre = self.__taille_espace + i * (self.__taille_tuile + self.__taille_espace) + self.__taille_tuile//2, #Coordonnée y du centre de la tuile
            valeur=0
            ) for j in range(4)] for i in range(4)]
        self.grille = copie_grille(self.__grille_zero) #On copie pour éviter tout bug (svp)
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
                self.grille[i][j].affiche(self.__canvas, True) #On affiche tuile par tuile
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
        
    def gauche(self, test = False) -> bool:
        """
        Tasse la grille sur la gauche et renvoie
        True or False si la grille a changée ou non.
        """
        changement , new_grille = gauche_grille(self.grille)
        if changement and not(test):
            #Si la grille a bougée, on ajoute 1 case et on actualise le score et la grille
            self.transition("gauche")
            self.grille = copie_grille(new_grille)
            self.score = add_random(grille = self.grille, score = self.score)
        return changement
        
    def droite(self, test = False) -> bool:
        """
        Tasse la grille sur la droite et renvoie
        True or False si la grille a changée ou non.
        """
        grille_rotated = copie_grille(self.grille)
        grille_rotated = rotation_horaire_grille(grille_rotated)
        grille_rotated = rotation_horaire_grille(grille_rotated)
        changement , new_grille = gauche_grille(grille_rotated)
        new_grille = copie_grille(new_grille)
        new_grille = rotation_horaire_grille(new_grille)
        new_grille = rotation_horaire_grille(new_grille)
        if changement and not(test):
            #Si la grille a bougée, on ajoute 1 case et on actualise le score et la grille
            self.transition("droite")
            self.grille = copie_grille(new_grille)
            self.score = add_random(grille = self.grille, score = self.score)
        
        return changement

    def haut(self, test = False) -> bool:
        """
        Tasse la grille sur le haut et renvoie
        True or False si la grille a changée ou non.
        """
        grille_rotated = copie_grille(self.grille)
        grille_rotated = rotation_horaire_grille(grille_rotated)
        grille_rotated = rotation_horaire_grille(grille_rotated)
        grille_rotated = rotation_horaire_grille(grille_rotated)
        changement , new_grille = gauche_grille(grille_rotated)
        new_grille = copie_grille(new_grille)
        new_grille = rotation_horaire_grille(new_grille)
        if changement and not(test):
            #Si la grille a bougée, on ajoute 1 case et on actualise le score et la grille
            self.transition("haut")
            self.grille = copie_grille(new_grille)
            self.score = add_random(grille = self.grille, score = self.score)
        
        return changement

    def bas(self, test = False) -> bool:
        """
        Tasse la grille sur le bas et renvoie
        True or False si la grille a changée ou non.
        """
        grille_rotated = copie_grille(self.grille)
        grille_rotated = rotation_horaire_grille(grille_rotated)
        changement , new_grille = gauche_grille(grille_rotated)
        new_grille = copie_grille(new_grille)
        new_grille = rotation_horaire_grille(new_grille)
        new_grille = rotation_horaire_grille(new_grille)
        new_grille = rotation_horaire_grille(new_grille)
        if changement and not(test):
            #Si la grille a bougée, on ajoute 1 case et on actualise le score et la grille
            self.transition("bas")
            self.grille = copie_grille(new_grille)
            self.score = add_random(grille = self.grille, score = self.score)
        
        return changement

    def verif(self) -> bool:
        """
        Vérifie s'il est possible d'effectuer un mouvement.
        Renvoie True or False
        """
        for move in [self.droite, self.gauche, self.haut, self.bas]:
            if move(test=True):
                #Si un mouvement est possible, on remet la grille et le score d'origine
                #Rem : pas la peine d'actualiser la grille si move()=False
                return True
        return False
    
    
    def transition(self , direction):
        grille_valeur = []
        for i in range(4):
            row = []
            for j in range(4):
                row.append(self.grille[i][j].valeur)
            grille_valeur.append(row)
        
        if direction == "haut":
            grille_valeur = rotation_horaire_matrice(grille_valeur)
            grille_valeur = rotation_horaire_matrice(grille_valeur)
            grille_valeur = rotation_horaire_matrice(grille_valeur)
        elif direction=="bas":
            grille_valeur = rotation_horaire_matrice(grille_valeur)
        elif direction=="droite":
            grille_valeur = rotation_horaire_matrice(grille_valeur)
            grille_valeur = rotation_horaire_matrice(grille_valeur)
        
        grille_deplacement=[]
        d_max=1
        for i in range(4):
            l = parcours_liste(grille_valeur[i])
            for j in l:
                if j!=None:
                    d_max = max(d_max , abs(j[0] - j[1]))
            grille_deplacement.append(l)
        
        if direction == "haut":
            grille_deplacement = rotation_horaire_matrice(grille_deplacement)
        elif direction=="bas":
            grille_deplacement = rotation_horaire_matrice(grille_deplacement)
            grille_deplacement = rotation_horaire_matrice(grille_deplacement)
            grille_deplacement = rotation_horaire_matrice(grille_deplacement)
        elif direction=="droite":
            grille_deplacement = rotation_horaire_matrice(grille_deplacement)
            grille_deplacement = rotation_horaire_matrice(grille_deplacement)
        
        grille_parcours = []
        for i in range(4):
            row = []
            for j in range(4):
                if grille_deplacement[i][j]!=None:
                    n=0
                    if direction=="haut" or direction=="bas":
                        n = j
                    elif direction=="gauche" or direction=="droite":
                        n = i
                    row.append(parcours(
                        indice_initial = grille_deplacement[i][j][0],
                        indice_final = grille_deplacement[i][j][1],
                        sens_tassage = direction,
                        n = n,
                        n_images = self.n_images,
                        d_max = d_max
                        ))
                else:
                    row.append(None)
            grille_parcours.append(row)
            
        grille_copy = copie_grille(self.grille)
        
        l_taille=[]
        for i in range(4):
            for j in range(4):
                if grille_deplacement[i][j]!=None:
                    if grille_deplacement[i][j][2]==True:
                        grille_copy[i][j].valeur = grille_copy[i][j].valeur * 2
                        l_taille.append((i,j))
        
        for image in range(self.n_images):
            self.__canvas.delete("all") #On efface tout
            for i in range(4):
                for j in range(4):
                    self.__grille_zero[i][j].affiche(self.__canvas, False) #On affiche tuile par tuile
            if direction=="droite":
                for j in range(4):
                    for i in range(4):
                        if grille_parcours[i][j]!=None:
                            grille_copy[i][j].x = grille_parcours[i][j][image][0]
                            grille_copy[i][j].y = grille_parcours[i][j][image][1]
                            test=True
                            for k in l_taille:
                                if k[0]==i and k[1]==j:
                                    test=False
                            grille_copy[i][j].affiche(self.__canvas, test)
            if direction=="gauche":
                for j in range(4):
                    for i in range(4):
                        if grille_parcours[i][3-j]!=None:
                            grille_copy[i][3-j].x = grille_parcours[i][3-j][image][0]
                            grille_copy[i][3-j].y = grille_parcours[i][3-j][image][1]
                            test=True
                            for k in l_taille:
                                if k[0]==i and k[1]==3-j:
                                    test=False
                            grille_copy[i][3-j].affiche(self.__canvas, test)
            if direction=="bas":
                for i in range(4):
                    for j in range(4):
                        if grille_parcours[i][j]!=None:
                            grille_copy[i][j].x = grille_parcours[i][j][image][0]
                            grille_copy[i][j].y = grille_parcours[i][j][image][1]
                            test=True
                            for k in l_taille:
                                if k[0]==i and k[1]==j:
                                    test=False
                            grille_copy[i][j].affiche(self.__canvas, test)
            if direction=="haut":
                for i in range(4):
                    for j in range(4):
                        if grille_parcours[3-i][j]!=None:
                            grille_copy[3-i][j].x = grille_parcours[3-i][j][image][0]
                            grille_copy[3-i][j].y = grille_parcours[3-i][j][image][1]
                            test=True
                            for k in l_taille:
                                if k[0]==3-i and k[1]==j:
                                    test=False
                            grille_copy[3-i][j].affiche(self.__canvas, test)
            
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
            time.sleep(self.tps1)
        
        if len(l_taille)>0:
            for image in range(self.n_images):
                self.__canvas.delete("all") #On efface tout
                for i in range(4):
                    for j in range(4):
                        self.__grille_zero[i][j].affiche(self.__canvas, False) #On affiche tuile par tuile
                for i in range(4):
                    for j in range(4):
                        if grille_copy[i][j].valeur!=0 and not([i,j] in l_taille):
                            grille_copy[i][j].affiche(self.__canvas, True)
                if image<self.n_images//2:
                    grossissement_police = 1.2 * (image / (self.n_images//2))
                    nv_taille = 100 + 20 * (image / (self.n_images // 2))
                else:
                    grossissement_police = 1.2 - 0.2 * (image / self.n_images)
                    nv_taille = 120 - 20 * (image / self.n_images)
                for k in l_taille:
                    i = k[0]
                    j = k[1]
                    grille_copy[i][j].taille = round(nv_taille)
                    grille_copy[i][j].affiche(self.__canvas, True, grossissement_police)
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
                time.sleep(self.tps2)
        
    
    
    def fin_du_jeu(self) -> None:
        """
        Ferme le jeu.
        """
        self.__canvas.create_rectangle(0,self.__taille_grille,self.__taille_grille,self.__taille_grille+100, fill="#BBADA0",width=0)
        self.__canvas.create_text(self.__taille_grille//2,self.__taille_grille+30, text="Game over !", font=("Helvetica", 24, "bold"), fill="black")
        self.__canvas.create_text(self.__taille_grille//2,self.__taille_grille+60, text=f"Score final : {self.score}", font=("Helvetica", 24, "bold"), fill="black")
        self.__root.mainloop() #On laisse la fenêtre ouverte