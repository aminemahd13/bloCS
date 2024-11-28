def coord_to_screen(x : int , y : int , player) -> tuple:
    x = x - player.x_left() + player.get_x_screen()
    y = y - player.y_up() + player.get_y_screen()
    return x, y

def screen_to_coord(x_screen: int, y_screen: int, player) -> tuple:
    x = x_screen - player.get_x_screen() + player.x_left()
    y = y_screen - player.get_y_screen() + player.y_up()
    return x, y

def coord_to_indice(x : int , y : int) -> tuple:
    if x >= 0:
        x_indice = x // 40
    else:
        x = -x
        x_indice = x // 40
        x_indice = -x_indice - 1
    if y >= 0:
        y_indice = y // 40
    else:
        y = -y
        y_indice = y // 40
        y_indice = -y_indice - 1
    
    return x_indice , y_indice


def indice_to_coord(x_indice : int , y_indice : int) -> tuple:
    return x_indice * 40 , y_indice * 40


def indice_to_screen(x_indice : int , y_indice : int , player) -> tuple:
    x , y = indice_to_coord(x_indice = x_indice , y_indice = y_indice)
    return coord_to_screen(x = x , y = y , player = player)

def screen_to_indice(x_screen : int , y_screen : int , player) -> tuple:
    x , y = screen_to_coord(x_screen = x_screen , y_screen = y_screen , player = player)
    return coord_to_indice(x = x , y = y)