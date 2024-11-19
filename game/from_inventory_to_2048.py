def est_tuile(obj):
    #Vérifie si l'objet donné est une instance de la classe Tuile.  
    # :param obj: L'objet à vérifier.
    # :return: True si c'est une Tuile, sinon False.

    return isinstance(obj, Tuile)



def inventory_to_2048(inventory,Grille,i): 
    #prend en paramètre un inventaire, une gtille et un rang d'un element dans l'inventaire
    if est_tuile(inventory[i])== True : #on verifie que l'objet est une tuile
        Grille.add_tuile(inventory[i])


