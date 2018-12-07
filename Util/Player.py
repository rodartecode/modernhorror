import discord

class Player(discord.User):
    def __init__(self):
        self.temperment = 50
        self.progress = 0

    def getTemp(self):
        return self.temperment

    def getProgress(self):
        return self.progress

    