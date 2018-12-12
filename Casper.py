import os
import discord
from discord.ext import commands
import asyncio
import xml.etree.ElementTree as et
from Util import servermanager, messagemanager
TOKEN = ''

client = discord.Client()
bot = commands.Bot(command_prefix = "!")

basePath = os.path.dirname(os.path.realpath(__file__))
casperFile =  os.path.join(basePath, "Data\\Casper.xml")
## Check that the file path is correct
print(casperFile)

tree = et.parse(casperFile)
root = tree.getroot()
for elem in root:
    print(elem.tag, elem.text)
    for e in elem:
        print (e.tag, e.text)
        for child in e:
            print(child.tag, child.text)

class Stats:
    is_running = False
    option = 0
    temperment = 0
    player = None
    messman = None
    messageArray = ["Ok, no turning back now! \nSo, are you a man or a woman?",
                    ".....A MANLY MAN!", "A LADAYYY!!!", "...a dog???", "Hey, it's you, Casper!" ]

options = Stats()
perms = servermanager.ServerManager(client)


@client.event
async def on_ready():
    print("The bot is ready!")
    await client.change_presence(game=discord.Game(name="Making a bot"))

@client.event
async def on_member_join(member):
    options.player = member
    await perms.serverSetup(member)
    options.messman = messagemanager.MessageManager(client)
    startingPoint = await perms.getChannelByName(name="aether", server=member.server)
    msg = await client.send_message(startingPoint, "Hello there...")
    await start_loop(msg)

@client.event
async def on_message(message):
    MSG = message.content.upper()

    if options.messman != None:
        await options.messman.enqueue(message, message.server)
    else:
        print("messman is none")

    if message.author == client.user:
        return
    if MSG == "HELLO":
        await client.send_message(message.channel, "World")
    if message.content == "START" or message.content == "start":
        if options.is_running == False:
            options.option = 0
            options.is_running = True
            message.author
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
    print("starting loop")

    if options.option == 0:
        intro_dialog = []
        print("finding lines")
        intro_dialog = root.findall("./Scene[@id='0']/Option[@id='0']/line")
        intro_text = []
        print("size of lines: ", len(intro_dialog))

        for elem in intro_dialog:
            print(elem.text)
            intro_text.append(elem.text)

        if len(intro_dialog) == 0:
            print("uh-oh")
        else:
            print("huh? what?")
            print(len(intro_dialog))

        for line in intro_text:
            print(">", line)
        
        print("done finding lines")


        await client.send_message(message.channel, intro_text[0])
        emb = (discord.Embed(description=intro_text[1], colour = 0x3DF270))
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