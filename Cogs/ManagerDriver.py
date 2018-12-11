##############################################
##############################################
#    THIS IS MY TEST FILE FOR RUNNING UNPROTECTED SCRIPTS
#    IT IS NOT ADVISABLE TO LOOK TOO CLOSELY LEST THE
#    CODE LOOKS BACK AT YE
##############################################
##############################################


import sys
import os
import asyncio
import DataLoader
import discord
import time
import json

from collections import namedtuple
import discord.ext.commands as cmd

# We'll inherit the extended commands.Bot
# And base our main bot from this class
class Bot(cmd.Bot):
    def __init__(self, *args, prefix=None, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_message(self, msg):
        if not self.is_ready() or msg.author.bot:
            return

        await self.process_commands(msg)
# Helper class to load our JSON files

def get(file):
    try:
        with open(file, encoding='utf8') as data:
            return json.load(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    except AttributeError:
        raise AttributeError("Unknown argument")
    except FileNotFoundError:
        raise FileNotFoundError("JSON file wasn't found")

# Helper class to get the current date
def date(target, clock=True):
    if clock is False:
        return target.strftime("%d %B %Y")
    return target.strftime("%d %B %Y, %H:%M")





class GameManagerDriver:

    ## this is constant variable, please no change
    ## "constant" var: how long to wait before sending
    ## msg in delayedMessage method ~jr    
    DEFAULT_WAIT = 2

    ## Instantiate DataLoader
    Loader = DataLoader.DataLoader()

    ## constructor?? I guess its probably not called 
    ## that in python. initializer? 
    ## This loads a reference to the bot and stores 
    ## it.
    ##      ~jr
    def __init__(self, client):
        self.client = client
        self.config = get("game_config.json")
        
        # Get the dialog lists
        self.player_text = GameManagerDriver.Loader.setupPlayer()
        self.player_text = GameManagerDriver.Loader.setupBot()

        # A list of the current players in the server
        self.players = []

        # A list of channels to be used in server
        # channel_list is an array of tuples
        channel_list = self.config.channels
        channel_names = []
        
        # Get the channel name strings 
        for elem in channel_list:
            print(elem[0])
            channel_names.append(elem[0])

        # A list of all servers the bot is a part of
        self.joined_servers = client.guilds

        for server in self.joined_servers:
            serv_members = server.members
            
            print("list of member ids:")
            for memb in serv_members:
                print(memb.id)


# Create Bot
bot = Bot(command_prefix=config.prefix, prefix=config.prefix)

test = bot
driver = GameManagerDriver(test)
bot.run(config.crow_token)



test.close()