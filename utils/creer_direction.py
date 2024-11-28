import utils.key_handler as key

def creer_direction(dict_touches):
    dict_touches["right"] = key.right()
    dict_touches["left"] = key.left()
    dict_touches["up"] = key.up()
    dict_touches["echap"] = key.close()
    dict_touches["number"] = key.get_number()
    