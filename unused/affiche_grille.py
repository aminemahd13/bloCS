THEMES = {
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
# Le thème va de "0" à "2"


def longueur_max(grille: list, theme: str) -> int:
    """
    Renvoie la longueur maximale de caractère sur la grille
    en fonction du thème choisi.
    """
    global THEMES
    mx = 0
    for i in range(4):
        for j in range(4):
            car = THEMES[theme][grille[i][j]]  # Caractere en fonction du thème
            longueur = len(car)  # Longueur du caractère
            if longueur > mx:  # Si longueur plus grande que max
                mx = longueur  # On actualise
    return mx


def grid_to_string(grille: list, theme: str) -> str:
    """
    Renvoie une chaîne de caractères correspondant à la grille
    en fonction du thème choisi.
    """
    global THEMES
    grille_modif = grille
    n = longueur_max(grille=grille, theme=theme)
    for i in range(4):
        for j in range(4):
            car = THEMES[theme][grille[i][j]]
            longueur = n - len(car)  # Nombre d'espaces à rajouter
            # On rajoute les espaces équitablement
            if longueur % 2 == 0:
                grille_modif[i][j] = longueur // 2 * " " + car + longueur // 2 * " "
            else:
                grille_modif[i][j] = (
                    longueur // 2 * " " + car + (longueur // 2 + 1) * " "
                )

    tiret = (n + 2) * "-"  # Nombre de "-" à mettre pour bien afficher la grille
    a = f"""
     {tiret} {tiret} {tiret} {tiret}
    | {grille_modif[0][0]} | {grille_modif[0][1]} | {grille_modif[0][2]} | {grille_modif[0][3]} |
     {tiret} {tiret} {tiret} {tiret}
    | {grille_modif[1][0]} | {grille_modif[1][1]} | {grille_modif[1][2]} | {grille_modif[1][3]} |
     {tiret} {tiret} {tiret} {tiret}
    | {grille_modif[2][0]} | {grille_modif[2][1]} | {grille_modif[2][2]} | {grille_modif[2][3]} |
     {tiret} {tiret} {tiret} {tiret}
    | {grille_modif[3][0]} | {grille_modif[3][1]} | {grille_modif[3][2]} | {grille_modif[3][3]} |
     {tiret} {tiret} {tiret} {tiret}
        """
    return a


grille = [[2048, 16, 32, 0], [0, 4, 0, 2], [0, 0, 0, 32], [512, 1024, 0, 2]]
theme = "0"
print(grid_to_string(grille=grille, theme=theme))
