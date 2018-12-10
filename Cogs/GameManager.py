import sys
import os
import asyncio
from Cogs import DataLoader
from Util import Default, Repo, Player
import discord
from discord.ext import commands


class GameManager:

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
        self.config = Default.get("game_config.json")
        
        # Get the dialog lists
        self.player_text = GameManager.Loader.setupPlayer()
        self.player_text = GameManager.Loader.setupBot()

        # A dictionary of the current players in the server
        self.players = []]

        # A list of channels to be used in server
        # channel_list is an array of tuples
        channel_list = self.config.channels
        channel_names = []
        
        # Get the channel name strings 
        for elem in channel_list:
            print(elem[0])
            channel_names.append(elem[0])

        




    async def on_ready(self):
        print(type(self.client))

        # A list of all servers the bot is a part of
        self.joined_servers = self.client.servers

        for server in self.joined_servers:
            serv_members = server.members
            
            print("list of member ids:")
            for memb in serv_members:
                print(memb.id)

                if (Repo.memb_is_owner(memb.id)):
                    pass
                elif (self.players[f"{memb.id}"]):
                    pass
                else:
                    pass

                    
        print("GM ready")


    # Sends a message after a specified amount of time
    # Right now it uses a global default variable, but
    # can be changed to accept another argument for seconds
    async def delayedMessage(self, message):
        if(not message):
            print("There's no message")
            return

        msg = message.content
        print(f"message loaded as: {msg}")
        await asyncio.sleep(GameManager.DEFAULT_WAIT)
        print(f"slept for {GameManager.DEFAULT_WAIT} seconds")
        await self.client.send_message(message.channel, msg)

    async def start_loop(self):
        pass
        



def setup(client):
    client.add_cog(GameManager(client))

