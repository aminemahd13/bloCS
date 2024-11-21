from game.utils.ajout_aleatoire import add_random_tuile
from game.utils.gauche import gauche_ligne, gauche_grille
from game.utils.parcours_liste_gauche import parcours_liste
from game.utils.parcours import parcours
from game.utils.copie import copie_tuile, copie_ligne, copie_grille, copie_matrice
from game.utils.rotation import rotation_horaire_grille, rotation_horaire_matrice, rotation_antihoraire_grille, rotation_antihoraire_matrice, rotation_double_grille, rotation_double_matrice
from game.utils.cancel_transition import cancel_transition, creation_hist_touches
from game.classes.classetuile import Tuile
import tkinter as tk
import time

class Grille:
    def __init__(self):
        self.n_images1 = 20 #Nombre d'images lors du déplacement d'une tuile au maximum
        self.n_images2 = 16 #Nombre d'images lors d'une fusion
        self.tps = 0.0008 #Temps entre les images (fixe les fps)
        self.__taille_tuile = 100 #Taille d'une tuile en px
        self.__taille_espace = 10 #Taille d'un espace en px
        #Taille de la grille
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
        
    def affiche(self , inventory : dict) -> None:
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
            self.__taille_grille + 20, #Coordonnée y
            text = text_score,
            font = ("Helvetica", 18, "bold"),
            fill = "black"
            )
        self.__root.update() #On actualise la fenêtre graphique
        
    def gauche(self, test = False) -> bool:
        """
        Tasse la grille sur la gauche et renvoie
        True or False si la grille a changée ou non.
        test, initialement sur False, indique s'il faut changer la grille ou non.
        """
        #On crée une copie de la grille tassée à gauche
        changement , new_grille = gauche_grille(self.grille)
        if changement and not(test): #Si la grille a bougée et qu'on ne fait pas de test
            self.transition("gauche") #On affiche la transition
            self.grille = copie_grille(new_grille) #On actualise la grille
        return changement
        
    def droite(self, test = False) -> bool:
        """
        Tasse la grille sur la droite et renvoie
        True or False si la grille a changée ou non.
        test, initialement sur False, indique s'il faut changer la grille ou non.
        """
        #On crée une copie de la grille tassée à droite
        grille_rotated = copie_grille(self.grille)
        grille_rotated = rotation_double_grille(grille_rotated)
        changement , new_grille = gauche_grille(grille_rotated)
        new_grille = rotation_double_grille(new_grille)
        if changement and not(test):
            self.transition("droite")
            self.grille = copie_grille(new_grille)
        return changement

    def haut(self, test = False) -> bool:
        """
        Tasse la grille sur le haut et renvoie
        True or False si la grille a changée ou non.
        test, initialement sur False, indique s'il faut changer la grille ou non.
        """
        #On crée une copie de la grille tassée en haut
        grille_rotated = copie_grille(self.grille)
        grille_rotated = rotation_antihoraire_grille(grille_rotated)
        changement , new_grille = gauche_grille(grille_rotated)
        new_grille = rotation_horaire_grille(new_grille)
        if changement and not(test):
            self.transition("haut")
            self.grille = copie_grille(new_grille)
        return changement

    def bas(self, test = False) -> bool:
        """
        Tasse la grille sur le bas et renvoie
        True or False si la grille a changée ou non.
        test, initialement sur False, indique s'il faut changer la grille ou non.
        """
        #On crée une copie de la grille tassée en bas
        grille_rotated = copie_grille(self.grille)
        grille_rotated = rotation_horaire_grille(grille_rotated)
        changement , new_grille = gauche_grille(grille_rotated)
        new_grille = rotation_antihoraire_grille(new_grille)
        if changement and not(test):
            self.transition("bas")
            self.grille = copie_grille(new_grille)
        return changement

    def verif(self) -> bool:
        """
        Vérifie s'il est possible d'effectuer un mouvement.
        Renvoie True or False
        """
        for move in [self.droite, self.gauche, self.haut, self.bas]:
            if move(test=True): #On indique que c'est un test et qu'il ne faut pas modifier la grille
                return True
        return False
    
    
    def transition(self , direction : str) -> bool:
        """
        Effectue une animation de transition entre
        la grille actuelle et la prochaine grille.
        Renvoie si la transition a été annulée ou non.
        """
        #On regarde les touches dans leur état initial
        hist_touches = creation_hist_touches()
        stop_transition = False
        #On crée une grille constitué des valeurs entières de la grille
        grille_valeur = []
        for i in range(4):
            row = []
            for j in range(4):
                row.append(self.grille[i][j].valeur)
            grille_valeur.append(row)
        
        #On la tourne pour faire les opérations à gauche
        if direction == "haut":
            grille_valeur = rotation_antihoraire_matrice(grille_valeur)
        elif direction=="bas":
            grille_valeur = rotation_horaire_matrice(grille_valeur)
        elif direction=="droite":
            grille_valeur = rotation_double_matrice(grille_valeur)
        
        #On regarde le déplacement de chacune des tuiles (en terme d'indices) sur sa ligne
        #et on crée une grille contenant ces infos
        grille_deplacement=[]
        d_max = 0
        for i in range(4):
            ligne = parcours_liste(grille_valeur[i])
            for deplacement in ligne:
                if deplacement is not None:
                    #Déplacement maximal (en terme d'indices) 
                    d_max = max(d_max , abs(deplacement[0] - deplacement[1]))
            grille_deplacement.append(ligne)
        
        if d_max != 0: #S'il n'y a pas de déplacement, on ne fait pas la suite
            #On multiplie par un facteur pour ajuster la durée de transition en fonction
            #Du déplacement max
            n_images1 = self.n_images1 * d_max // 4
            
            #On remet la grille de déplacements dans le bon sens
            if direction == "haut":
                grille_deplacement = rotation_horaire_matrice(grille_deplacement)
            elif direction=="bas":
                grille_deplacement = rotation_antihoraire_matrice(grille_deplacement)
            elif direction=="droite":
                grille_deplacement = rotation_double_matrice(grille_deplacement)
            
            #On crée une matrice contenan, pour chaque (i,j), une liste de coordonnées (x,y) indiquant leur parcours
            grille_parcours = []
            for i in range(4):
                row = []
                for j in range(4):
                    if grille_deplacement[i][j] is not None:
                        #n = numéro de ligne si on tasse selon les lignes
                        #n = numéro de colonne si on tasse selon les colonnes
                        if direction in ["haut", "bas"]:
                            n = j
                        elif direction in ["gauche", "droite"]:
                            n = i
                        row.append(parcours(
                            indice_initial = grille_deplacement[i][j][0],
                            indice_final = grille_deplacement[i][j][1],
                            sens_tassage = direction,
                            n = n,
                            n_images = n_images1
                            ))
                    else:
                        row.append(None)
                grille_parcours.append(row)
                
            grille_copy = copie_grille(self.grille)
            
            #On crée une liste l_taille contenant tout les (i,j) des tuiles qui vont grossir l_taille
            #Et une liste contenant toutes les tuiles qui vont se faire "absorber"
            l_taille=[]
            l_absorb=[]
            for i in range(4):
                for j in range(4):
                    if grille_deplacement[i][j] is not None:
                        if grille_deplacement[i][j][2]==1:
                            grille_copy[i][j].valeur = grille_copy[i][j].valeur * 2
                            l_taille.append((i,j))
                        elif grille_deplacement[i][j][2]==2:
                            l_absorb.append((i,j))
            
            #On affiche les grilles qui bougent image par image
            for image in range(n_images1):
                if not(stop_transition): #On vérifie si l'utilisateur veut stopper la transition ou non
                    stop_transition = stop_transition or cancel_transition(hist_touches)
                
                if not(stop_transition): #Si l'utilisateur ne veut pas stopper la transition
                    self.__canvas.delete("all") #On efface tout
                    #On affiche un arrière plan de cases vides
                    for i in range(4):
                        for j in range(4):
                            self.__grille_zero[i][j].affiche(self.__canvas, False) #On affiche tuile par tuile
                    
                    #On distinct les 4 cas de directions, car ceux-ci imposent différentes règles
                    #Au niveau des premiers/arrières plans
                    if direction=="droite": #On affiche d'abord les tuiles sur la gauche (en arrière plan)
                        for j in range(4):
                            for i in range(4):
                                if grille_parcours[i][j] is not None:
                                    #On effectue le "déplacement élémentaire" de la tuile
                                    grille_copy[i][j].x = grille_parcours[i][j][image][0]
                                    grille_copy[i][j].y = grille_parcours[i][j][image][1]
                                    #On affiche le chiffre uniquement si la tuile ne va pas grossir pour fusion
                                    affiche_chiffre = True
                                    if (i,j) in l_taille:
                                        affiche_chiffre = False
                                    grille_copy[i][j].affiche(self.__canvas, affiche_chiffre)
                    if direction=="gauche": #On affiche d'abord les tuiles sur la droite (en arrière plan)
                        for j in range(4):
                            j = 3 - j
                            for i in range(4):
                                if grille_parcours[i][j] is not None:
                                    #On effectue le "déplacement élémentaire" de la tuile
                                    grille_copy[i][j].x = grille_parcours[i][j][image][0]
                                    grille_copy[i][j].y = grille_parcours[i][j][image][1]
                                    #On affiche le chiffre uniquement si la tuile ne va pas grossir pour fusion
                                    affiche_chiffre = True
                                    if (i,j) in l_taille:
                                        affiche_chiffre = False
                                    grille_copy[i][j].affiche(self.__canvas, affiche_chiffre)
                    if direction=="bas": #On affiche d'abord les tuiles sur le haut (en arrière plan)
                        for i in range(4):
                            for j in range(4):
                                if grille_parcours[i][j] is not None:
                                    #On effectue le "déplacement élémentaire" de la tuile
                                    grille_copy[i][j].x = grille_parcours[i][j][image][0]
                                    grille_copy[i][j].y = grille_parcours[i][j][image][1]
                                    #On affiche le chiffre uniquement si la tuile ne va pas grossir pour fusion
                                    affiche_chiffre = True
                                    if (i,j) in l_taille:
                                        affiche_chiffre = False
                                    grille_copy[i][j].affiche(self.__canvas, affiche_chiffre)
                    if direction=="haut": #On affiche d'abord les tuiles sur le bas (en arrière plan)
                        for i in range(4):
                            i = 3 - i
                            for j in range(4):
                                if grille_parcours[i][j] is not None:
                                    #On effectue le "déplacement élémentaire" de la tuile
                                    grille_copy[i][j].x = grille_parcours[i][j][image][0]
                                    grille_copy[i][j].y = grille_parcours[i][j][image][1]
                                    #On affiche le chiffre uniquement si la tuile ne va pas grossir pour fusion
                                    affiche_chiffre = True
                                    if (i,j) in l_taille:
                                        affiche_chiffre = False
                                    grille_copy[i][j].affiche(self.__canvas, affiche_chiffre)
                    
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
                    time.sleep(self.tps)
            
            #On réalise les fusions en animation image par image
            if len(l_taille)>0:
                for image in range(self.n_images2):
                    if not(stop_transition): #On vérifie si l'utilisateur souhaite stopper la transition ou non
                        stop_transition = stop_transition or cancel_transition(hist_touches)
                    if not(stop_transition): #Si l'utilisateur ne veut pas stopper la transition
                        self.__canvas.delete("all") #On efface tout
                        #On met une grille remplie de zeros en arrière plan
                        for i in range(4):
                            for j in range(4):
                                self.__grille_zero[i][j].affiche(self.__canvas, False) #On affiche tuile par tuile
                        #On affiche les tuiles qui ne vont pas grossir ou se faire absorber
                        for i in range(4):
                            for j in range(4):
                                if grille_copy[i][j].valeur!=0 and (i,j) not in l_taille and (i,j) not in l_absorb:
                                    grille_copy[i][j].affiche(self.__canvas, True)
                        
                        if image<self.n_images2//2: #1ère partie de l'animation : on grossit
                            grossissement_police = 2.36 * image / self.n_images2
                            nv_taille = 100 + 36 * (image / self.n_images2)
                        else: #2ème partie de l'animation : on rétressit
                            grossissement_police = 1.36 - 0.36 * (image / self.n_images2)
                            nv_taille = 136 - 36 * (image / self.n_images2)
                        for (i,j) in l_taille: #On affiche les tuiles qui grossissent
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
                        time.sleep(self.tps)
        return stop_transition
    
    def add_tuile(self , valeur) -> bool:
        """
        Ajoute une tuile valeur aléatoirement.
        Renvoie True si la tuile a été ajoutée,
        False sinon.
        """
        score = self.score
        self.score = add_random_tuile(grille = self.grille , score = self.score , valeur = valeur)
        if self.score == score:
            return False
        return True
        
    def fermer_fenetre(self) -> None:
        """
        Ferme la fenêtre.
        """
        self.__canvas.destroy()
        self.__root.destroy()
    
    def ouvrir_fenetre(self) -> None:
        """
        Affiche la fenêtre.
        """
        # Configuration de la fenêtre principale
        self.__root = tk.Tk()
        self.__root.title("2048")
        self.__root.geometry(f"{self.__taille_grille}x{self.__taille_grille+100}")
        self.__root.config(bg="#BBADA0")
        # Crée un canvas pour dessiner la grille
        self.__canvas = tk.Canvas(self.__root, width=self.__taille_grille, height=self.__taille_grille+100, bg="#BBADA0")
        self.__canvas.pack()
        
    def fin_du_jeu(self) -> None:
        """
        Ferme le jeu.
        """
        self.__canvas.create_rectangle(0,self.__taille_grille,self.__taille_grille,self.__taille_grille+100, fill="#BBADA0",width=0)
        self.__canvas.create_text(self.__taille_grille//2,self.__taille_grille+30, text="Game over !", font=("Helvetica", 24, "bold"), fill="black")
        self.__canvas.create_text(self.__taille_grille//2,self.__taille_grille+60, text=f"Score final : {self.score}", font=("Helvetica", 24, "bold"), fill="black")
        self.__root.mainloop() #On laisse la fenêtre ouverte

