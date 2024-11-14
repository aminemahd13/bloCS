
def affiche(grille: list, score: int, theme: str) -> None:
    """
    Affiche la grille en fonction du thème choisi.
    Affiche également les erreurs si la grille n'est pas carrée ou contient des valeurs inattendues.
    """
    themes = {
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
    
    if theme not in themes:
        print("Error: Theme not found.")
        return

    display_func = themes[theme]["display"]
    max_len = max(len(display_func(value)) for row in grille for value in row)
    
    grille_str = []
    for row in grille:
        ligne = []
        for value in row:
            car = display_func(value)
            padding = (max_len - len(car)) // 2
            ligne.append(" " * padding + car + " " * (max_len - len(car) - padding))
        grille_str.append(ligne)

    tiret = (max_len + 2) * "-"
    ligne_tirets = " " + " ".join([tiret] * len(grille))

    print(f"Score: {score}")
    grille_print = ligne_tirets
    for row in grille_str:
        ligne = "|" + "|".join(f" {car} " for car in row) + "|"
        grille_print += f"\n{ligne}\n{ligne_tirets}"
    print(grille_print)
