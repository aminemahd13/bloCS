import unittest
from affiche import affiche
from classegrille import Grille
from classegrille import copie

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
