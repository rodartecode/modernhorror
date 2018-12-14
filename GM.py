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
    def __init__(self, client, game_config, database):
        self.client = client
        self.messman = None

        ## Game configs
        print("Fetching config file")
        self.config = game_config
        print("config loaded")
        print("Fetching player database")
        self.db = database
        print("Db loaded")
        
        # Get the dialog lists
        self.player_text = GM.Loader.setupPlayer()
        self.player_text1 = GM.Loader.setupPlayer2()
        self.bot_text = GM.Loader.setupBot()
        self.bot_text = GM.Loader.setupBot2()
        print('Dialog loaded')

        # A dictionary of the current players in the server
        self.players = {}
        print('Players dictionary initialized')

        # Check db and load players who have played the game
        print("loading db")
        for i in self.db:
            if i not in self.players:
                new_id = i
                self.players[new_id] = self.db[i]

        # A list of channels to be used in server
        # channel_list is an array of tuples
        self.channel_list = self.config['channels']
        self.channel_dict = self.config['channel_dict']
        self.channel_names = []
        chty = type(self.channel_dict)
        print(chty)
        print(self.channel_dict['aether'])
        
        

        

        print("GameManager initialized")
