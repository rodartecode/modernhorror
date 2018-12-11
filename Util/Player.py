import discord
import json


class Player(discord.User):

    # initializer accepts optional arguments we can use to
    # load player progress
    def __init__(self, newUserId = 0, newProgress = 0, newTemp = 50, newDialog = []):
        self.temperment = newTemp
        self.progress = newProgress
        self.dialog_list = newDialog
        self.user_id = newUserId

    def serialize_player(self):
        return {
            "__player__": True,
            "user_id": self.user_id,
            "progress": self.progress,
            "temperment": self.temperment
        }


###########

def encode_player(dct):
    if "__player__" in dct:
        return Player(dct['progress'], dct['user_id'], dct['temperment'])
    else:
        return dct

    


    