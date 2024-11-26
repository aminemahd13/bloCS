import utils.key_handler as key

def creer_direction(hist_touches):
    if key.right() and (not hist_touches["right"] or not key.left()):
            direction = "right"
    elif key.left() and (not hist_touches["left"] or not key.right()):
        direction = "left"
    else:
        direction = None
    wanna_jump = key.up()
    
    return direction , wanna_jump