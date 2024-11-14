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
        self.grille = copie(grille_zero)
        self.theme = theme
        self.taille = taille
        self.score = 0
        n = (taille * taille) // 8
        for _ in range(n):
            self.score = add_random(grille=self.grille, score=self.score)

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


# Unit Tests
import unittest

class TestGrille(unittest.TestCase):

    def test_copie(self):
        grille = [[1, 2], [3, 4]]
        copie_grille = copie(grille)
        self.assertEqual(grille, copie_grille)
        self.assertIsNot(grille, copie_grille)

    def test_affiche(self):
        grille = [[2, 4], [8, 16]]
        score = 100
        try:
            affiche(grille, score, theme="0")
            affiche(grille, score, theme="1")
            affiche(grille, score, theme="2")
        except Exception as e:
            self.fail(f"affiche function raised an exception: {e}")

    def test_gauche(self):
        grille_obj = Grille(taille=2, theme="0")
        grille_obj.grille = [[2, 2], [4, 4]]
        self.assertTrue(grille_obj.gauche())
        self.assertEqual(grille_obj.grille, [[4, 0], [8, 0]])

    def test_verif(self):
        grille_obj = Grille(taille=2, theme="0")
        grille_obj.grille = [[2, 4], [8, 16]]
        self.assertTrue(grille_obj.verif())

if __name__ == "__main__":
    unittest.main()
