import ajout_aleatoire
import gauche

add_random = ajout_aleatoire.add_random
gauche_ligne = gauche.gauche_ligne


def copie(grille: list) -> list:
    """
    Copie terme à terme le tableau.
    """
    grille_copie = []  # Création d'un tableau vide
    for i in range(len(grille)):
        # On copie terme à terme chaque ligne
        ligne = []
        for j in range(len(grille)):
            ligne.append(grille[i][j])
        grille_copie.append(ligne)  # On ajoute la ligne dans la copie
    return grille_copie


class Grille:
    def __init__(self, taille: int, theme: str):
        grille_zero = [[0 for i in range(taille)] for i in range(taille)]
        self.grille = copie(grille_zero)  # Création d'un tableau vide
        self.theme = theme
        self.taille = taille
        self.score = 0
        self.__dict_themes = {
            "0": {
                "name": "Default",
                0: "",
                2: "2",
                4: "4",
                8: "8",
                16: "16",
                32: "32",
                64: "64",
                128: "128",
                256: "256",
                512: "512",
                1024: "1024",
                2048: "2048",
                4096: "4096",
                8192: "8192",
            },
            "1": {
                "name": "Chemistry",
                0: "",
                2: "H",
                4: "He",
                8: "Li",
                16: "Be",
                32: "B",
                64: "C",
                128: "N",
                256: "O",
                512: "F",
                1024: "Ne",
                2048: "Na",
                4096: "Mg",
                8192: "Al",
            },
            "2": {
                "name": "Alphabet",
                0: "",
                2: "A",
                4: "B",
                8: "C",
                16: "D",
                32: "E",
                64: "F",
                128: "G",
                256: "H",
                512: "I",
                1024: "J",
                2048: "K",
                4096: "L",
                8192: "M",
            },
        }
        n = (taille * taille) // 8  # On rempli initialement 1/8 de la grille
        for i in range(n):
            # On ajoute des nombres randoms et on met le score
            self.score = add_random(grille=self.grille, score=self.score)

    def _longueur_max(self) -> int:
        """
        Donne la longueur maximale de caractères de la grille
        en fonction du thème (fonction cachée).
        """
        m = 0
        for i in range(self.taille):
            for j in range(self.taille):
                ch = self.grille[i][j]
                l = len(self.__dict_themes[self.theme][ch])
                if l > m:
                    m = l
        return m

    def affiche(self) -> None:
        """
        Affiche la grille en fonction
        du thème choisi.
        """
        grille_str = []  # Grille contenant les caractères "graphiques"
        n = self._longueur_max()  # Longueur à utiliser dans les cases
        for i in range(self.taille):
            ligne = []  # Ligne contenant les caractères
            for j in range(self.taille):
                car = self.__THEMES[self.theme][self.grille[i][j]]
                longueur = n - len(car)  # Nombre d'espaces à rajouter
                # On rajoute les espaces équitablement pour combler
                if longueur % 2 == 0:
                    ligne.append(longueur // 2 * " " + car + longueur // 2 * " ")
                else:
                    ligne.append(longueur // 2 * " " + car + (longueur // 2 + 1) * " ")
            grille_str.append(ligne)

        tiret = (n + 2) * "-"  # Nombre de "-" à mettre pour bien afficher la grille
        # Création de T, une ligne qui sépare les cases
        ligne_tirets = " "
        for i in range(self.taille - 1):  # On crée les cases
            ligne_tiret = ligne_tiret + str(tiret) + " "
        ligne_tiret = ligne_tiret + str(tiret)

        # Création de la chaine de caractères G pour afficher la grille
        grille_str = ligne_tiret
        for i in range(self.taille):
            # Création d'une liste L contenant les caractères des cases etc
            ligne = "|"
            for j in range(self.taille):
                ligne = ligne + " " + str(grille_str[i][j]) + " |"
            # On met L et T dans la grille
            grille_str = grille_str + "\n" + ligne + "\n" + ligne_tiret
        print(grille_str)  # Affichage de la grille

    def gauche(self) -> bool:
        """
        Tasse la grille à gauche et renvoie True ou False
        s'il y a eu un changement ou non.
        """
        changement = False  # Initialement pas de changements
        grille = copie(self.grille)
        for i in range(self.taille):
            ligne = grille[i]
            gauche_ligne(L)  # On tasse la ligne
            grille[i] = ligne
            if ligne != self.grille[i]:
                changement = True  # Passe à True au moindre changement de ligne

        if changement:
            # On actualise la grille et le score, et on ajoute des cases
            self.grille = copie(grille)
            self.score = add_random(grille=self.grille, score=self.score)

        return changement

    def _rotation_horaire(self) -> None:
        """
        Tourne la grille dans le sens horaire.
        """
        matrice_rotated = [
            [0] * self.taille for _ in range(self.taille)
        ]  # Crée une matrice vide de même taille

        for i in range(self.taille):
            for j in range(self.taille):
                matrice_rotated[j][self.taille - i - 1] = self.grille[i][j]

        self.grille = matrice_rotated

    def droite(self) -> bool:
        """
        Tasse la grille à droite et renvoie True ou False
        s'il y a eu un changement ou non.
        """
        self._rotation_horaire()
        self._rotation_horaire()
        changement = self.gauche()
        self._rotation_horaire()
        self._rotation_horaire()
        return changement

    def haut(self) -> bool:
        """
        Tasse la grille en haut et renvoie True ou False
        s'il y a eu un changement ou non.
        """
        self._rotation_horaire()
        self._rotation_horaire()
        self._rotation_horaire()
        changement = self.gauche()
        self._rotation_horaire()
        return changement

    def bas(self) -> None:
        """
        Tasse la grille en bas et renvoie True ou False
        s'il y a eu un changement ou non.
        """
        self._rotation_horaire()
        changement = self.gauche()
        self._rotation_horaire()
        self._rotation_horaire()
        self._rotation_horaire()
        return changement

    def verif(self) -> bool:
        """
        Renvoie True si le jeu peut continuer,
        False sinon.
        """
        grille = copie(self.grille)
        score = self.score

        if self.droite():  # Si la grille a bougée en tassant à droite
            self.grille = grille
            self.score = score
            return True  # Un mouvement est bel et bien possible
        # La grille n'a pas bougée

        if self.gauche():  # Si la grille a bougée en tassant à gauche
            self.grille = grille
            self.score = score
            return True  # Un mouvement est bel et bien possible
        # La grille n'a pas bougée

        if self.haut():  # Si la grille a bougée en tassant en haut
            self.grille = grille
            self.score = score
            return True  # Un mouvement est bel et bien possible
        # La grille n'a pas bougée

        if self.bas():  # Si la grille a bougée en tassant en bas
            self.grille = grille
            self.score = score
            return True  # Un mouvement est bel et bien possible
        # La grille n'a pas bougée

        return False
