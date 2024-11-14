import ajout_aleatoire
import gauche

add_random = ajout_aleatoire.add_random
gauche_ligne = gauche.gauche_ligne


def copie(grille: list) -> list:
    """
    Copie terme à terme le tableau.
    """
    return [row[:] for row in grille]


class Grille:
    def __init__(self, taille: int, theme: str):
        grille_zero = [[0 for _ in range(taille)] for _ in range(taille)]
        self.grille = copie(grille_zero)  # Création d'un tableau vide
        self.theme = theme
        self.taille = taille
        self.score = 0
        self.__dict_themes = {
            "0": {
                "name": "Default",
                "display": lambda x: str(x) if x > 0 else "",
            },
            "1": {
                "name": "Chemistry",
                "display": lambda x: ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al"][x.bit_length() - 1] if 1 <= x.bit_length() <= 13 else str(x),
            },
            "2": {
                "name": "Alphabet",
                "display": lambda x: chr(64 + x.bit_length()) if 1 <= x.bit_length() <= 26 else str(x),
            },
        }
        n = (taille * taille) // 8  # On rempli initialement 1/8 de la grille
        for _ in range(n):
            self.score = add_random(grille=self.grille, score=self.score)

    def _longueur_max(self) -> int:
        """
        Donne la longueur maximale de caractères de la grille
        en fonction du thème (fonction cachée).
        """
        max_len = 0
        display_func = self.__dict_themes[self.theme]["display"]
        for row in self.grille:
            for value in row:
                max_len = max(max_len, len(display_func(value)))
        return max_len

    def affiche(self) -> None:
        """
        Affiche la grille en fonction
        du thème choisi.
        """
        display_func = self.__dict_themes[self.theme]["display"]
        max_len = self._longueur_max()
        
        grille_str = []
        for row in self.grille:
            ligne = []
            for value in row:
                car = display_func(value)
                padding = (max_len - len(car)) // 2
                ligne.append(" " * padding + car + " " * (max_len - len(car) - padding))
            grille_str.append(ligne)

        tiret = (max_len + 2) * "-"
        ligne_tirets = " " + " ".join([tiret] * self.taille)

        grille_print = ligne_tirets
        for row in grille_str:
            ligne = "|" + "|".join(f" {car} " for car in row) + "|"
            grille_print += f"\n{ligne}\n{ligne_tirets}"
        print(grille_print)

    def gauche(self) -> bool:
        """
        Tasse la grille à gauche et renvoie True ou False
        s'il y a eu un changement ou non.
        """
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
        """
        Tourne la grille dans le sens horaire.
        """
        self.grille = [[self.grille[self.taille - j - 1][i] for j in range(self.taille)] for i in range(self.taille)]

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
