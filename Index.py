import os
import discord
from Util.Data import Bot
from discord.ext.commands import HelpFormatter
from Util import Default

print(discord.__version__)
# Parse the json config file
config = Default.get("game_config.json")
db = Default.get_player_db("db.json")

# Create Bot
bot = Bot(command_prefix=config['prefix'], prefix=config['prefix'])

print("Starting extensions loop")
# This for loop loads all the cogs
for file in os.listdir("Cogs"):
    if file.endswith(".py"):        
        # This trims the '.py' off the end of the file name
        name = file[:-3]        
        try:
            # Check that the cog is in our cogs list in game_config.json
            if name in config['cogs']:
                print(f"Trying to load extension {name}")
                bot.load_extension(f"Cogs.{name}")
                print(f"{name} loaded.")
            else:
                print(f"{name} was NOT loaded")
        except Exception as e:
            try:
                bot.unload_extension(f"Cogs.{name}")
            except Exception as exc:
                print(f"That didn't work: {exc}")
            print(f'{file} cannot be loaded: {e}')
        
# Run the bot with crow_token
bot.run(config['crow_token'])
