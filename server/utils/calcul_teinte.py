from math import cos , pi

def calculer_teinte(compteur_frame , fps):
    # Durée totale d'une journée en frames
    total_frames = 24 * fps
    
    # Calcul de la teinte
    teinte = int(127.5 * (1 + cos(2 * pi * (compteur_frame - 1) / total_frames)))
    return teinte