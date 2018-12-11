import time
import json
from Util import Player

from collections import namedtuple


class PlayerDecoder(json.JSONEncoder):
    def default(self, obj):
        # pylint: disable=E0202
        # ^^ my linter does not like me overriding this
        # encoder so that comment actually does something

        # If it's a Player object it returns a dictionary with
        # relevant data
        if (isinstance(obj, Player.Player)):
            return {
                "__player__": True,
                "user_id": obj.user_id,
                "progress": obj.progress,
                "temperment": obj.temperment
            }
        else:
            return json.JSONEncoder.default(self, obj)    

# Helper class to load our JSON files
def get(file):
    try:
        with open(file, encoding='utf8') as data:
            return json.load(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    except AttributeError:
        raise AttributeError("Unknown argument")
    except FileNotFoundError:
        raise FileNotFoundError(f"1a JSON file {file} wasn't found")

# Same function but this parses our player database into 
# "Player" python objects
def get_player_db(file):
    try:
        with open(file, encoding='utf8') as data:
            return json.load(data, object_hook=Player.encode_player)
    except AttributeError:
        raise AttributeError("Unknown argument")
    except FileNotFoundError:
        raise FileNotFoundError(f"1b JSON file {file} was not found")


def put_player_db(data, file):
    try:
        player_dict = dict(data)
        with open(file, 'w', encoding='utf8') as player_data:
            json.dump(player_dict, player_data, cls=PlayerDecoder)
    except AttributeError:
        raise AttributeError("Unkown argument in put_player_db")
    except FileNotFoundError:
        raise FileNotFoundError(f"2b JSON file {file} not found")

# Helper class to get the current date
def date(target, clock=True):
    if clock is False:
        return target.strftime("%d %B %Y")
    return target.strftime("%d %B %Y, %H:%M")