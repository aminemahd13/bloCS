class ManyType:
    def __init__(self , liste_types):
        self.liste_types = liste_types
    def contains(self , value):
        if value is None:
            if None in self.liste_types:
                return True
        elif type(value) in self.liste_types:
            return True
        elif type(value) == list:
            for liste in self.liste_types:
                if type(liste) == list:
                    if verif_list_global(value , liste):
                        return True
            return False
        elif type(value) == dict:
            for dictionnaire in self.liste_types:
                if type(dictionnaire) == dict:
                    if verif_dict_global(value , dictionnaire):
                        return True
            return False
        elif type(value) == tuple:
            for tupl in self.liste_types:
                if type(tupl) == tuple:
                    if verif_tuple_global(value , tupl):
                        return True
            return False
        return False
def verif_dict_global(data , data_type):
    try:
        if type(data) != dict:
            return False
        any_type = 0
        any_condition = None
        key_done = []
        for key , value in data_type.items():
            if type(key) != type:
                if key not in data:
                    return False
                if type(value) == type:
                    if type(data[key]) != value:
                        return False
                elif type(value) == dict:
                    if not verif_dict_global(data[key] , value):
                        return False
                elif type(value) == list:
                    if not verif_list_global(data[key] , value):
                        return False
                elif type(value) == ManyType:
                    if not value.contains(data[key]):
                        return False
                elif type(value) == tuple:
                    if not verif_tuple_global(data[key] , value):
                        return False
                else:
                    return False
                key_done.append(key)
            else:
                any_type = key
                any_condition = value
                break
        if any_type == 0:
            if len(data) != len(data_type):
                return False
        else:
            dict_a_verif = {key : data[key] for key in data if key not in key_done}
            for key in dict_a_verif:
                if type(key) != any_type:
                    return False
            dict_type = {key : any_condition for key in dict_a_verif}
            if not verif_dict_global(dict_a_verif , dict_type):
                return False
        return True
    except Exception:
        return False
def verif_list_global(liste , liste_type):
    try:
        if type(liste) != list:
            return False
        if len(liste) != len(liste_type):
            return False
        for i , value in enumerate(liste_type):
            if type(value) == type:
                if type(liste[i]) != value:
                    return False
            elif type(value) == dict:
                if not verif_dict_global(liste[i] , value):
                    return False
            elif type(value) == list:
                if not verif_list_global(liste[i] , value):
                    return False
            elif type(value) == ManyType:
                if not value.contains(liste[i]):
                    return False
            elif type(value) == tuple:
                if not verif_tuple_global(liste[i] , value):
                    return False
            else:
                return False
        return True
    except Exception:
        return False
def verif_tuple_global(tupl , tuple_type):
    try:
        if type(tupl) != tuple:
            return False
        if len(tupl) != len(tuple_type):
            return False
        for i , value in enumerate(tuple_type):
            if type(value) == type:
                if type(tupl[i]) != value:
                    return False
            elif type(value) == dict:
                if not verif_dict_global(tupl[i] , value):
                    return False
            elif type(value) == list:
                if not verif_list_global(tupl[i] , value):
                    return False
            elif type(value) == ManyType:
                if not value.contains(tupl[i]):
                    return False
            elif type(value) == tuple:
                if not verif_tuple_global(tupl[i] , value):
                    return False
            else:
                return False
        return True
    except Exception:
        return False





data_received_type = {
    "right" : bool,
    "left" : bool,
    "up" : bool,
    "echap" : bool,
    "number" : int,
    "click" : ManyType([None , [int , int , int]])
}

def verif_data_received(data , height , width):
    if verif_dict_global(data , data_received_type):
        if data["click"] is not None:
            if not (0<=data["click"][0]<=width and 0<=data["click"][1]<=height and data["click"][2] in [1,3]):
                return False
        if not(0<=data["number"]<=4):
            return False
        return True
    return False

data_client_request_type = {
    "name" : str,
    "height" : int,
    "width" : int
}

def verif_client_request(data):
    if verif_dict_global(data , data_client_request_type):
        if not(0<=data["height"]<=1080 and 0<=data["width"]<=1920):
            return False
        return True
    return False