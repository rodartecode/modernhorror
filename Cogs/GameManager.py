import sys
import os
sys.path.append(os.path.abspath('../Util'))
import DataLoader
import asyncio
import discord
from discord.ext import commands


class GameManager:

    ## this is constant variable, please no change
    ## "constant" var: how long to wait before sending
    ## msg in delayedMessage method ~jr    
    DEFAULT_WAIT = 2

    Loader = DataLoader()

    ## constructor?? I guess its probably not called 
    ## that in python. initializer? 
    ## This loads a reference to the bot and stores 
    ## it.
    ##      ~jr
    def __init__(self, client):
        self.client = client
        self.player_text = GameManager.Loader.setupPlayer()
        self.player_text = GameManager.Loader.setupBot()

    ## Sends a discord message after DEFAULT_WAIT
    ## number of seconds ~jr

    async def delayedMessage(self, message):
        if(not message):
            print("There's no message")
            return

        msg = message.content
        print(f"message loaded as: {msg}")
        await asyncio.sleep(GameManager.DEFAULT_WAIT)
        print(f"slept for {GameManager.DEFAULT_WAIT} seconds")
        await self.client.send_message(message.channel, msg)

def setup(client):
    client.add_cog(GameManager(client))


Manager = GameManager()
