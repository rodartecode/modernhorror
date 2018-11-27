import discord
from discord.ext import commands
import asyncio

TOKEN = ''

client = discord.Client()
bot = commands.Bot(command_prefix = "!")

class Stats:
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
    if message.author == client.user:
        return
    if message.content == "Hello":
        await client.send_message(message.channel, "World")
    if message.content == "Start" or message.content == "start":
        options.option = 0
        await start_loop(message)
    if message.content == "Die":
        exit()
    if message.content == "Reset":
        options.option = 0


@client.event
async def start_loop(message):
    emojispam = ['👨', '👩', '🐕', '👻']

    if options.option == 0:
        await client.send_message(message.channel, "Ok, no turning back now! \nSo, are you a man or a woman?")
        emb = (discord.Embed(description="👨: You choose a man \n👩: You choose a woman \n🐕: You choose a dog \n👻: You choose a ghost", colour = 0x3DF270))
        funmsg = await client.send_message(message.channel, embed=emb)
        
        """this loop adds the reactions"""
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