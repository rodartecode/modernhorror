import os

from Util.Data import Bot
from discord.ext.commands import HelpFormatter
from Util import Default

config = Default.get("game_config.json")
print(config)
bot = Bot(command_prefix=config.prefix, prefix=config.prefix)


for file in os.listdir("Cogs"):
    if file.endswith(".py"):        
        try:
            name = file[:-3]
            print(name)
            if name in config.cogs:
                print("Trying to load extension")
                bot.load_extension(f"Cogs.{name}")
                print(f"{name} loaded.")
            else:
                print(f"{name} was NOT loaded")
        except Exception as e:
            print(f'{file} cannot be loaded: {e}')
        

bot.run(config.crow_token)
