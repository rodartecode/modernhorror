import discord

class Player(discord.User):

    # initializer accepts optional arguments we can use to
    # load player progress
    def __init__(self, newDialog, newTemp = 50, newProgress = 0):
        self.temperment = newTemp
        self.progress = newProgress
        self.dialog_list = newDialog

    # GETTERS
    ################################
    def getTemp(self):
        return self.temperment

    def getProgress(self):
        return self.progress

    