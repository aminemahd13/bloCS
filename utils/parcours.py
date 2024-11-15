def parcours(indice_initial : int , indice_final : int, sens_tassage : str , n : int , n_images : int) -> list:
    dp = 3 * (100 + 10) / n_images
    P = []
    
    if sens_tassage=="gauche":
        xi , xf = 10 + 50 + indice_initial * (100 + 10) , 10 + 50 + indice_final * (100 + 10)
        x = xi
        y = 10 + 50 + n * (100 + 10)
        for _ in range(n_images):
            x = max(x - dp , xf)
            P.append((x , y))
    
    if sens_tassage=="droite":
        xi , xf = 10 + 50 + (3 - indice_initial) * (100 + 10) , 10 + 50 + (3 - indice_final) * (100 + 10)
        x = xi
        y = 10 + 50 + n * (100 + 10)
        for _ in range(n_images):
            x = min(x + dp , xf)
            P.append((x , y))
    
    if sens_tassage=="haut":
        yi , yf = 10 + 50 + indice_initial * (100 + 10) , 10 + 50 + indice_final * (100 + 10)
        y = yi
        x = 10 + 50 + n * (100 + 10)
        for _ in range(n_images):
            y = max(y - dp, yf)
            P.append((x , y))
    
    if sens_tassage=="bas":
        yi , yf = 10 + 50 + (3 -indice_initial) * (100 + 10) , 10 + 50 + (3 -indice_final) * (100 + 10)
        y = yi
        x = 10 + 50 + n * (100 + 10)
        for _ in range(n_images):
            y = min(y + dp, yf)
            P.append((x , y))
    
    return P