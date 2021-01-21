from copy import deepcopy

message_utils = {
    "game_exit": {
        "mount": False,
        "type": "game",
        "subtype": "exit"
    },
    "game_att_request": {
        "mount": False,
        "type": "game",
        "subtype": "att_request"
    },
    "game_end": {
        "mount": False,
        "type": "game",
        "subtype": "end",
    },
    "game_init": {
        "mount": True,
        "type": "game",
        "subtype": "init",
        "id_room": None
    },
    "game_make_play": {
        "mount": True,
        "type": "game",
        "subtype": "make_play",
        "text": None
    },
    "menu_create": {
        "mount": True,
        "type": "menu",
        "subtype": "create",
        "name_player": None,
        "name_room": None,
        "password": None
    },
    "menu_enter": {
        "mount": True,
        "type": "menu",
        "subtype": "enter",
        "name_player": None,
        "id_room": None,
        "password": None
    },
    "menu_end": {
        "mount": False,
        "type": "menu",
        "subtype": "end"
    },
    "room": {
        "mount": False,
        "type": "room",
        "subtype": "exit"
    },
}


def mount_message(type_, args=None):
    try:
        aux = deepcopy(message_utils[type_])
    except KeyError:
        raise Exception("Error in type of message.")

    test = aux["mount"]

    if test and args is None:
        raise Exception("Args is necessary!")

    del aux["mount"]

    if not test:
        return aux

    count = 0
    for i in aux:
        if aux[i] is None:
            aux[i] = args[count]
            count += 1

    if count < len(args):
        raise Exception("Problem when mount message. Insufficient args!")

    return aux

def check_type(value, type_check):
    if type(type_check) != type:
        raise RuntimeError("The parameters of check_type must be a value and type. "
                           f"Error (value: {type(value)}, type_check: type{type_check})")

    if type(value) != type_check:
        raise ValueError(f"The type must be a {type_check}")
