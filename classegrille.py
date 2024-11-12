from random import randint

def add_random(grille : dict) -> None:
    pass #A définir

class Grille() :
    def __init__(self , taille : int , theme : str) :
        L = [0 for i in range(taille)]
        self.liste = [L for i in range(taille)]
        self.theme = theme
        self.taille = taille
        self.__THEMES = {"0" : {"name" : "Default" , 0 : "" , 2 : "2" , 4 : "4" , 8 : "8" , 16 : "16" , 32 : "32" , 64 : "64" , 128 : "128" , 256 : "256" , 512 : "512" , 1024 : "1024" , 2048 : "2048" , 4096 : "4096" , 8192 : "8192"} , "1" : {"name" : "Chemistry" , 0 : "" , 2 : "H" , 4 : "He" , 8 : "Li" , 16 : "Be" , 32 : "B" , 64 : "C" , 128 : "N" , 256 : "O" , 512 : "F" , 1024 : "Ne" , 2048 : "Na" , 4096 : "Mg" , 8192 : "Al"} , "2" : {"name" : "Alphabet" , 0 : "" , 2 : "A" , 4 : "B" , 8 : "C" , 16 : "D" , 32 : "E" , 64 : "F" , 128 : "G" , 256 : "H" , 512 : "I" , 1024 : "J" , 2048 : "K" , 4096 : "L" , 8192 : "M"}}
        n = (taille * taille) // 8
        for i in range(n):
            add_random(grille = self.liste)
    
    def _longueur_max(self) -> int :
        """
        Donne la longueur maximale de caractères de la grille
        en fonction du thème (fonction cachée).
        """
        m = 0
        for i in range(self.taille):
            for j in range(self.taille):
                ch = self.liste[i][j]
                l = len(self.__THEMES[self.theme][ch])
                if l > m:
                    m = l
        return m
    
    def affiche(self) -> None :
        """
        Affiche la grille en fonction
        du thème choisi.
        """
        grille_modif = self.liste.copy() #Grille avec les caractèmes personnalisés
        n = self._longueur_max() #Longueur à utiliser dans les cases
        for i in range(self.taille):
            for j in range(self.taille):
                car = self.__THEMES[self.theme][self.liste[i][j]]
                longueur = n - len(car) #Nombre d'espaces à rajouter
                #On rajoute les espaces équitablement pour combler
                if longueur%2 == 0:
                    grille_modif[i][j] = longueur//2*" " + car + longueur//2*" "
                else:
                    grille_modif[i][j] = longueur//2*" " + car + (longueur//2+1)*" "
        
        tiret = (n+2)*"-" #Nombre de "-" à mettre pour bien afficher la grille
        #Création de T, une ligne qui sépare les cases
        T = " "
        for i in range(self.taille-1): #On crée les cases
            T = T + str(tiret) + " "
        T = T + str(tiret) 
        #Création de la chaine de caractères G pour afficher la grille
        G = T
        for i in range(self.taille):
            #Création d'une liste L contenant les caractères des cases etc
            L  ="|"
            for j in range(self.taille):
                L = L + " " + str(grille_modif[i][j]) + " |"
            #On met L et T dans la grille
            G = G + "\n" + L + "\n" + T
        print(G) #Affichage de la grille

    def verif_gauche(self) -> bool :
        """
        Renvoie True si la grille peut être tassée à gauche,
        False sinon.
        """
        return True #A définir
        #Renvoie True or False
    
    def gauche(self) -> None :
        """
        Tasse la grille à gauche.
        """
        pass #A définir
    
    def _rotation_horaire(self) -> None :
        """
        Tourne la grille dans le sens horaire.
        """
        pass #A définir
    
    def _rotation_antihoraire(self) -> None :
        """
        Tourne la grille dans le sens antihoraire.
        """
        pass #A définir
    
    def verif_droite(self) -> None :
        """
        Renvoie True si la grille peut être tassée à droite,
        False sinon.
        """
        self._rotation_horaire()
        self._rotation_horaire()
        test = self.verif_gauche()
        self._rotation_antihoraire()
        self._rotation_antihoraire()
        return test
    
    def droite(self) -> None :
        """
        Tasse la grille à droite.
        """
        self._rotation_horaire()
        self._rotation_horaire()
        self.gauche()
        self._rotation_antihoraire()
        self._rotation_antihoraire()
    
    def verif_haut(self) -> None :
        """
        Renvoie True si la grille peut être tassée en haut,
        False sinon.
        """
        self._rotation_antihoraire()
        test = self.verif_gauche()
        self._rotation_horaire()
        return test
    
    def haut(self) -> None :
        """
        Tasse la grille en haut.
        """
        self._rotation_antihoraire()
        self.gauche()
        self._rotation_horaire()
    
    def verif_bas(self) -> None :
        """
        Renvoie True si la grille peut être tassée en bas,
        False sinon.
        """
        self._rotation_horaire()
        test = self.verif_gauche()
        self._rotation_antihoraire()
        return test
    
    def bas(self) -> None :
        """
        Tasse la grille en bas.
        """
        self._rotation_horaire()
        self.gauche()
        self._rotation_antihoraire()