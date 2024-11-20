def coord_to_screen(block, player) -> tuple:
    x = block.x - player.x + player.x_screen
    y = block.y - player.y + player.y_screen
    return x, y

def screen_to_coord(x_screen: int, y_screen: int, player) -> tuple:
    x = (x_screen - player.x_screen + player.x) // 40 * 40 ## so the returned value is a multiple of 40 ie is a block :D
    y = (y_screen - player.y_screen + player.y) // 40 * 40
    return x, y
    