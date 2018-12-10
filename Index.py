import os
import discord
from Util.Data import Bot
from discord.ext.commands import HelpFormatter
from Util import Default

print(discord.__version__)
# Parse the json config file
config = Default.get("game_config.json")
print(config)

# Create Bot
bot = Bot(command_prefix=config.prefix, prefix=config.prefix)
typestring = type(bot)
print('type: ')
print(typestring)

# This for loop loads all the cogs
for file in os.listdir("Cogs"):
    if file.endswith(".py"):        
        try:
            # This trims the '.py' off the end of the file name
            name = file[:-3]
            # Check that the cog is in our cogs list in game_config.json
            if name in config.cogs:
                print("Trying to load extension")
                bot.load_extension(f"Cogs.{name}")
                print(f"{name} loaded.")
            else:
                print(f"{name} was NOT loaded")
        except Exception as e:
            print(f'{file} cannot be loaded: {e}')
        
# Run the bot with crow_token
bot.run(config.crow_token)
