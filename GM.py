import os
import asyncio
import discord
from Cogs import DataLoader
from Util import Default
class GM:
    # Some witchcraft to hardcode in the xml file paths
    # This file is gonna be full of repeating code
    # So this should be refactored into a few methods
    # and loops to automatically load all the files

    # For now, its hardcoded ~jr

    _basePath = os.path.dirname(os.path.realpath(__file__))

    _game_config_path = os.path.join('game_config.json')
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
        
        # Get the dialog lists
        self.player_text = GM.Loader.setupPlayer()
        self.player_text = GM.Loader.setupBot()

        # A dictionary of the current players in the server
        self.players = {}

        # Check db and load players who have played the game
        for i in self.db:
            if i['user_id'] not in self.players:
                new_id = i['user_id']
                self.players[new_id] = i

        # A list of channels to be used in server
        # channel_list is an array of tuples
        channel_list = [] #self.config.channels
        channel_names = []
        
        # Get the channel name strings 
        for elem in channel_list:
            print(elem[0])
            channel_names.append(elem[0])

test = GM(discord.client)

test.client.close()