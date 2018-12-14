import sys
import os
import asyncio
from Cogs import DataLoader
from Util import Default, Player
import discord
from discord.ext import commands


class GameManager:

    # Some witchcraft to hardcode in the file paths
    # For now, its hardcoded ~jr

    _basePath = os.path.dirname(os.path.realpath(__file__))
    _basePath = _basePath[:-4]
    _db_path = os.path.join(_basePath, "db.json")
    print(_db_path)

    #################################
    ## this is constant variables, please no change
    ## 
    ## how long to wait before sending
    ## msg in delayedMessage method ~jr    
    DEFAULT_WAIT = 2
    MODE = 1

    ##################################
    ## Instantiate DataLoader
    Loader = DataLoader.DataLoader()

    ## constructor?? I guess its probably not called 
    ## that in python. initializer? 
    ## This loads a reference to the bot and stores 
    ## it.
    ##      ~jr
    def __init__(self, client):
        self.client = client

        ## Game configs
        print("Fetching config file")
        self.config = Default.get("game_config.json")
        print("config loaded")
        print("Fetching player database")
        self.db = Default.get_player_db("db.json")
        print("Db loaded")
        
        # Get the dialog lists
        self.player_text = GameManager.Loader.setupPlayer()
        self.bot_text = GameManager.Loader.setupBot()
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

                if (memb.id in self.config['owners']):
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

        for serv in self.joined_servers:
                for ch in serv.channels:
                    if ch.id == self.channel_dict['aether']:
                        emb = (discord.Embed(description="text here"))
                        emb.set_image(url = "https://cdn.discordapp.com/attachments/520071023144599569/521500561279811597/aether2.jpg")
                        emb.set_author(name = self.bot_text[0])
                        print('aether')
                        await self.client.send_message(ch.id, self.bot_text[0])
                    if ch.id == self.channel_dict['attic']:
                        emb = (discord.Embed(description="text here"))
                        emb.set_image(url = "https://cdn.discordapp.com/attachments/518583486672535565/520023726742437888/attic.jpg")
                        emb.set_author(name = self.bot_text[0])
                        print('aether')
                        await self.client.send_message(ch, self.bot_text[0])



        await self.start_loop()
        print("GM ready")

    # END on_ready
    ##################################

    async def start_loop(self):
        if GameManager.MODE == 1:
            print('Starting game loop in MODE 1')



        elif GameManager.MODE == 2:
            print('Starting game loop in MODE 2')
        else:
            print('pass')

    async def on_reaction_add(self, reaction, user):
        pass


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
        



def setup(client):
    client.add_cog(GameManager(client))

