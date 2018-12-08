import discord

class Player(discord.User):
    def __init__(self, newTemp = 50, newProgress = 0, newDialog):
        self.temperment = newTemp
        self.progress = newProgress
        self.dialog_list = newDialog

    def getTemp(self):
        return self.temperment

    def getProgress(self):
        return self.progress

    