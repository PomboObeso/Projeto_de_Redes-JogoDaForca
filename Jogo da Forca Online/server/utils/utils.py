from copy import deepcopy
from random import randint

message_utils = {
    "game_init": {
        "mount": True,
        "type": "game",
        "subtype": "init",
        "status": None
    },
    "game_end": {
        "mount": False,
        "type": "game",
        "subtype": "end"
    },
    "game_alert": {
        "mount": True,
        "type": "game",
        "subtype": "alert",
        "message": None
    },
    "game_att_state": {
        "mount": True,
        "type": "game",
        "subtype": "att_state",
        "state": None
    }

}

all_words = ["BANANA"]


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
        raise Exception("The parameters of check_type must be a value and type. "
                           f"Error (value: {type(value)}, type_check: type{type_check})")

    if type(value) != type_check:
        raise ValueError(f"The type must be a {type_check}")


def words():
    drawn = randint(0, len(all_words) - 1)
    return all_words[drawn].upper()
