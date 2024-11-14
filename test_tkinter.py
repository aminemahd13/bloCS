import tkinter as tk

# Exemple de grille 4x4
grille = [
    [2, 4, 8, 16],
    [32, 64, 128, 256],
    [512, 1024, 2048, 4096],
    [0, 0, 0, 0]
]
score=5000

taille = 4

taille_tuile = 100
taille_espace = 10
taille_grille = taille * (taille_tuile + taille_espace) + taille_espace

# Couleurs pour chaque valeur de tuile
COULEURS_TUILE = {
    0: "#CDC1B4",
    2: "#EEE4DA",
    4: "#EDE0C8",
    8: "#F2B179",
    16: "#F59563",
    32: "#F67C5F",
    64: "#F65E3B",
    128: "#EDCF72",
    256: "#EDCC61",
    512: "#EDC850",
    1024: "#EDC53F",
    2048: "#EDC22E",
    4096: "#3C3A32"
}

# Configuration de la fenêtre principale
root = tk.Tk()
root.title("2048")
root.geometry(f"{taille_grille}x{taille_grille}")
root.config(bg="#BBADA0")

# Crée un canvas pour dessiner la grille
canvas = tk.Canvas(root, width=taille_grille, height=taille_grille+100, bg="#BBADA0")
canvas.pack()

def afficher_grille():
    canvas.delete("all")
    for i in range(taille):
        for j in range(taille):
            valeur = grille[i][j]
            x1, y1 = taille_espace + j * (taille_espace + taille_tuile) , taille_espace + i * (taille_espace + taille_tuile)
            x2, y2 = x1 + taille_tuile, y1 + taille_tuile
            couleur = COULEURS_TUILE.get(valeur, "#CDC1B4")
            canvas.create_rectangle(x1, y1, x2, y2, fill=couleur)
            if valeur != 0:
                if valeur<=4 :
                    canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=str(valeur), font=("Helvetica", 24, "bold"), fill="black")
                else:
                    canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=str(valeur), font=("Helvetica", 24, "bold"), fill="white")
    canvas.create_rectangle(0, taille_grille, taille_grille, taille_grille+100, fill="#BBADA0")
    text_score = "Score : "+str(score)
    canvas.create_text(taille_grille//2,taille_grille+50, text=text_score, font=("Helvetica", 24, "bold"), fill="black")


afficher_grille()
root.mainloop()

