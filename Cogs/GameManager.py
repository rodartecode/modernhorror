import sys
import os
import asyncio
from Cogs import DataLoader
from Util import Default, Player
import discord
from discord.ext import commands


class GameManager:

    # Some witchcraft to hardcode in the xml file paths
    # This file is gonna be full of repeating code
    # So this should be refactored into a few methods
    # and loops to automatically load all the files

    # For now, its hardcoded ~jr

    _basePath = os.path.dirname(os.path.realpath(__file__))
    _basePath = _basePath[:-4]

    _game_config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'game_config.json')
    _db_path = os.path.join(_basePath, "db.json")
    print(_game_config_path)
    print(_db_path)

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
        print("Fetching config file")
        self.config = Default.get("game_config.json")
        print("config loaded")
        print("Fetching player database")
        self.db = Default.get_player_db(self._db_path)
        print(self.db)
        print("Db loaded")
        
        # Get the dialog lists
        self.player_text = GameManager.Loader.setupPlayer()
        self.player_text = GameManager.Loader.setupBot()
        print('Dialog loaded')

        # A dictionary of the current players in the server
        self.players = {}
        print('Players dictionary initialized')

        typestring = type(self.db)
        # Check db and load players who have played the game
        print(typestring)
        print("loading db")
        for i in self.db:
            if i not in self.players:
                new_id = i
                self.players[new_id] = self.db[i]

        # A list of channels to be used in server
        # channel_list is an array of tuples
        channel_list = [] #self.config.channels
        channel_names = []
        
        # Get the channel name strings 
        for elem in channel_list:
            print(elem[0])
            channel_names.append(elem[0])

        print("GameManager initialized")
        

        




    async def on_ready(self):
        print(type(self.client))

        # A list of all servers the bot is a part of
        self.joined_servers = self.client.servers

        # This loops checks every member it sees in 
        # every server. First it checks if the member
        # user id is in the owners list in the config
        # then to see if the user exists in our database
        # and if they don't creates a new player for them 
        # and adds it to the list
        for server in self.joined_servers:                        
            print("list of member ids:")
            for memb in server.members:
                print(memb.id)

                if (memb.id in self.config.owners):
                    print(f"{memb.name} is an owner and will be assigned admin role")
                elif (memb.id in self.players):
                    print(f"{memb.name} is already in the database")
                else:
                    print(f"{memb.name} is a new player. Adding now.")
                    new_player = Player.Player(memb.id)
                    self.players[memb.id] = new_player.serialize_player()
                    print("Player added to self.players")
                    

        print("Updating database")
        Default.put_player_db(self.players, self._db_path)

        print("GM ready")

    # END on_ready
    ##################################



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

