import discord
import disc_config as cfg

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    author = message.author
    msg = message.content
    print('message received from {}: {}'.format(author, msg))

    if message.author == client.user:
        print('oops')
        return

    if message.content.startswith('$hello'):
        print('yay')
        await message.channel.send('Hello!')

client.run(cfg.disc_token)