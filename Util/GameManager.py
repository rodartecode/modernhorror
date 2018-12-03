import asyncio
import discord
from discord.ext import commands

class GameManager:

    ## this is constant variable, please no change
    ## constant for how long to wait before sending
    ## message in delayedMessage method ~jr    
    DEFAULT_WAIT = 2

    ## constructor?? I guess its probably not called 
    ## that in python ~jr
    def __init__(self):
        pass


    ## 
    ##

    async def delayedMessage(self, message):
        if(not message):
            print("There's no message")
            return

        msg = message
        await asyncio.sleep(GameManager.DEFAULT_WAIT)

