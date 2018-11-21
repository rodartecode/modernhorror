import discord
from discord.ext import commands
import asyncio

TOKEN = ''

client = discord.Client()
bot = commands.Bot(command_prefix = "!")

class Stats:
    option = 0
    temperment = 0

options = Stats()

@client.event
async def on_ready():
    print("The bot is ready!")

    await client.change_presence(game=discord.Game(name="Making a bot"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == "Hello":
        await client.send_message(message.channel, "World")
    if message.content == "Start" or message.content == "start":
        await start_loop(message)
    if message.content == "Die":
        exit()
    if message.content == "Reset":
        options.option = 0


@client.event
async def start_loop(message):
    if options.option == 0:
        await client.send_message(message.channel, "Ok, no turning back now!")
        await client.send_message(message.channel, "So, are you a man or a woman...")
        funmsg = await client.send_message(message.channel, "????")
        await client.add_reaction(funmsg, '👨')
        await client.add_reaction(funmsg, '👩')
        await client.add_reaction(funmsg, '🐕')
        await client.add_reaction(funmsg, '👻')

    elif options.option == 1:
        await client.send_message(message.channel, ".....A MANLY MAN!")
        options.option = 0
    elif options.option == 2:
        await client.send_message(message.channel, "A LADAYYY!!!")
        options.option = 0
    elif options.option == 3:
        options.option = 0
        await client.send_message(message.channel, ".....you like a cake?")
        unfunmsg = await client.send_message(message.channel, "????")
        await client.add_reaction(unfunmsg, '👍')
        await client.add_reaction(unfunmsg, '👎')
    elif options.option == 6:
        options.option = 0






    
@client.event
async def on_reaction_add(reaction, user):
    emojispam = ['👨', '👩', '🐕']
    if reaction.emoji == '👨' and reaction.count > 1:
         await client.send_message(reaction.message.channel, "A man!")
         options.option = 1
         await client.delete_message(reaction.message)
         await start_loop(reaction.message)
    if reaction.emoji == '👩' and reaction.count > 1:
         await client.send_message(reaction.message.channel, "A woman!")
         options.option = 2
         await client.delete_message(reaction.message)
         await start_loop(reaction.message)
    if reaction.emoji == '🐕' and reaction.count > 1:
         await client.send_message(reaction.message.channel, "A........ dog?")
         options.option = 3
         await client.delete_message(reaction.message)
         await start_loop(reaction.message)
    if reaction.emoji == '👍' and reaction.count > 1:
         await client.send_message(reaction.message.channel, "GOOOOOOOOO FUCK YOURSELLLLLLLLF!!!!!!!!!!")
         options.option = 4
         await client.delete_message(reaction.message)
         await start_loop(reaction.message)
    if reaction.emoji == '👎' and reaction.count > 1:
         await client.send_message(reaction.message.channel, "Oh I see. Have a nice day!")
         options.option = 5
         await client.delete_message(reaction.message)
         await start_loop(reaction.message)
    if reaction.emoji == '👻' and reaction.count > 1:
         await client.send_message(reaction.message.channel, "That's you, Casper!")
         options.option = 6
         await client.delete_message(reaction.message)
         await start_loop(reaction.message)



client.run(TOKEN)