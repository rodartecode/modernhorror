import discord
from discord.ext import commands
import disc_config as cfg

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    author = message.author
    msg = message.content
    channel = message.channel
    print('message received from {}: {}'.format(author, msg))

    if message.author == client.user:
        print('oops')
        return

    if message.content.startswith('hello'):
        print('yay')
        await client.send_message(channel, 'hello!')

client.run(cfg.disc_token)