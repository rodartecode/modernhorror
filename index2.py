import asyncio
import discord
from discord.ext.commands import Bot
import json
from Cogs import DataLoader
from Util import servermanager, messagemanager, Player
import GM



class PlayerDecoder(json.JSONEncoder):
    def default(self, obj):
        # pylint: disable=E0202
        # ^^ my linter does not like me overriding this
        # encoder so that comment actually does something

        # If it's a Player object it returns a dictionary with
        # relevant data
        if (isinstance(obj, Player.Player)):
            return {
                "__player__": True,
                "user_id": obj.user_id,
                "progress": obj.progress,
                "temperment": obj.temperment
            }
        else:
            return json.JSONEncoder.default(self, obj)    

# Helper class to load our JSON files
def get(file):
    try:
        with open(file, 'r', encoding='utf8') as data:
            return json.load(data)
    except AttributeError:
        raise AttributeError("Unknown argument")
    except FileNotFoundError:
        raise FileNotFoundError(f"1a JSON file {file} wasn't found")

# Same function but this parses our player database into 
# "Player" python objects
def get_player_db(file):
    try:
        with open(file, encoding='utf8') as data:
            return json.load(data, object_hook=Player.encode_player)
    except AttributeError:
        raise AttributeError("Unknown argument")
    except FileNotFoundError:
        raise FileNotFoundError(f"1b JSON file {file} was not found")


def put_player_db(data, file):
    try:
        player_dict = dict(data)
        with open(file, 'w', encoding='utf8') as player_data:
            json.dump(player_dict, player_data, cls=PlayerDecoder)
    except AttributeError:
        raise AttributeError("Unkown argument in put_player_db")
    except FileNotFoundError:
        raise FileNotFoundError(f"2b JSON file {file} not found")


# Parse the json config file
config = get("game_config.json")
db = get_player_db("db.json")

# Create Bot
bot = discord.Client()
manager = GM.GM(bot, config, db)
perms = servermanager.ServerManager(bot)

@bot.event
async def on_ready():
        print(type(manager.client))

        # A list of all servers the bot is a part of
        manager.joined_servers = manager.client.servers

        # This loops checks every member it sees in 
        # every server. First it checks if the member
        # user id is in the owners list in the config
        # then to see if the user exists in our database
        # and if they don't creates a new player for them 
        # and adds it to the list
        for server in manager.joined_servers:                        
            print("list of member ids:")
            for memb in server.members:
                print(memb.id)

                if (memb.id in manager.config['owners']):
                    print(f"{memb.name} is an owner and will be assigned admin role")
                elif (memb.id in manager.players):
                    print(f"{memb.name} is already in the database")
                else:
                    print(f"{memb.name} is a new player. Adding now.")
                    new_player = Player.Player(memb.id)
                    manager.players[memb.id] = new_player.serialize_player()
                    print("Player added to self.players")
                    

        print("Updating database")
        put_player_db(manager.players, manager._db_path)

        manager.messman = messagemanager.MessageManager(manager.client)

        print("GM ready")

bot.run(config['crow_token'])
