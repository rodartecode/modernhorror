import discord
import discord.ext.commands as cmd

# We'll inherit the extended commands.Bot
# And base our main bot from this class
class Bot(cmd.Bot):
    def __init__(self, *args, prefix=None, **kwargs):
        super(Bot, self).__init__(*args, **kwargs)

    async def on_message(self, msg):
        if not self.is_ready() or msg.author.bot:
            return

        await self.process_commands(msg)