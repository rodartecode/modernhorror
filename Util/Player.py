import discord
import json


class Player(discord.User):

    # initializer accepts optional arguments we can use to
    # load player progress
    def __init__(self, newProgress = 0, newUserId = 0, newTemp = 50, newDialog = []):
        self.temperment = newTemp
        self.progress = newProgress
        self.dialog_list = newDialog
        self.user_id = newUserId


    #######

class PlayerDecoder(json.JSONEncoder):
    def default(self, obj):
        # pylint: disable=E0202
        # ^^ my linter does not like me overriding this
        # encoder so that comment actually does something

        # If it's a Player object it returns an array with
        # relevant data
        if (isinstance(obj, Player)):
            return 
            {
                "__player__": True
                "user_id": obj.user_id,
                "progress": obj.progress,
                "temperment": obj.temperment
            }
        else:
            return json.JSONEncoder.default(self, obj)    

def encode_as_player(dct):
    if "__player__" in dct:
        return Player(dct['progress'], dct['user_id'], dct['temperment'])
    else:
        return dct



    