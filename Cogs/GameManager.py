import asyncio
import discord
from discord.ext import commands

class GameManager:

    ## this is constant variable, please no change
    ## "constant" var: how long to wait before sending
    ## msg in delayedMessage method ~jr    
    DEFAULT_WAIT = 2

    ## constructor?? I guess its probably not called 
    ## that in python. initializer? 
    ## This loads a reference to the bot and stores 
    ## it.
    ##      ~jr
    def __init__(self, client):
        self.client = client


    ## Sends a discord message after DEAFULT_WAIT
    ## number of seconds ~jr

    async def delayedMessage(self, message):
        if(not message):
            print("There's no message")
            return

        msg = message.content
        print(f"message loaded as: {msg}")
        await asyncio.sleep(GameManager.DEFAULT_WAIT)
        await self.client.send_message(message.channel, msg)

def setup(client):
    client.add_cog(GameManager(client))