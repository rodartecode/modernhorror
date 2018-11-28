import os
import discord
from discord.ext import commands
import asyncio
import xml.etree.ElementTree as et
import disc_config as cfg
TOKEN = cfg.disc_token

client = discord.Client()
bot = commands.Bot(command_prefix = "!")

basePath = os.path.dirname(os.path.realpath(__file__))
casperFile =  os.path.join(basePath, "Data\\Casper.xml")
## Check that the file path is correct
print(casperFile)

class Stats:
    is_running = False
    option = 0
    temperment = 0
    messageArray = ["Ok, no turning back now! \nSo, are you a man or a woman?",
                    ".....A MANLY MAN!", "A LADAYYY!!!", "...a dog???", "Hey, it's you, Casper!" ]

options = Stats()


@client.event
async def on_ready():
    print("The bot is ready!")
    await client.change_presence(game=discord.Game(name="Making a bot"))

@client.event
async def on_message(message):
    MSG = message.content.upper()

    if message.author == client.user:
        return
    if MSG == "HELLO":
        await client.send_message(message.channel, "World")
    if message.content == "START" or message.content == "start":
        if options.is_running == False:
            options.option = 0
            options.is_running = True
            await start_loop(message)
            
    if MSG == "DIE":
        print("Casper is Dead")
        await client.close()
    if message.content == "RESET":
        options.option = 0
        options.is_running = False


@client.event
async def start_loop(message):
    emojispam = ['👨', '👩', '🐕', '👻']

    if options.option == 0:
        await client.send_message(message.channel, "Ok, no turning back now! \nSo, are you a man or a woman?")
        emb = (discord.Embed(description="👨: You choose a man \n👩: You choose a woman \n🐕: You choose a dog \n👻: You choose a ghost", colour = 0x3DF270))
        funmsg = await client.send_message(message.channel, embed=emb)
        
        ##this loop adds the reactions
        for emoji in emojispam:
            await client.add_reaction(funmsg, emoji)

    elif options.option == 3:
        options.option = 0
        await client.send_message(message.channel, ".....you like a cake?")
        unfunmsg = await client.send_message(message.channel, "????")
        await client.add_reaction(unfunmsg, '👍')
        await client.add_reaction(unfunmsg, '👎')
    
    else:
        await client.send_message(message.channel, options.messageArray[options.option])
        options.option = 0

    
    
@client.event
async def on_reaction_add(reaction, user):

    if reaction.emoji == '👨' and reaction.count > 1:
         options.option = 1
         await client.delete_message(reaction.message)
         await start_loop(reaction.message)

    if reaction.emoji == '👩' and reaction.count > 1:

         options.option = 2
         await client.delete_message(reaction.message)
         await start_loop(reaction.message)

    if reaction.emoji == '🐕' and reaction.count > 1:
         options.option = 3
         await client.delete_message(reaction.message)
         await start_loop(reaction.message)

    if reaction.emoji == '👻' and reaction.count > 1:
         options.option = 4
         await client.delete_message(reaction.message)
         await start_loop(reaction.message)

    if reaction.emoji == '👍' and reaction.count > 1:
         await client.send_message(reaction.message.channel, "GOOOOOOOOO FUCK YOURSELLLLLLLLF!!!!!!!!!!")
         options.option = 5
         await client.delete_message(reaction.message)
         await start_loop(reaction.message)

    if reaction.emoji == '👎' and reaction.count > 1:
         await client.send_message(reaction.message.channel, "Oh I see. Have a nice day!")
         options.option = 6
         await client.delete_message(reaction.message)
         await start_loop(reaction.message)


client.run(TOKEN)