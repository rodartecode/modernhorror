import asyncio
import discord
from discord.ext.commands import Bot
import json
import time
from Cogs import DataLoader
from Util import servermanager, messagemanager, Player
import GM


class IHoldThings():
    scene = 1
    progress = 0
    botprogress = 0
    player = None
    currentServer = None
    messMan = None


uglyBotArray = ["You hear someone coming up the stairs. It’s a family along with the realtor. They look very innocent and wholesome. Almost too much. You hear that they’re called the Smiths? That figures. They should be easy to scare off… Why do you want to scare them off? It just seems right. Maybe that’s just what ghosts do, like an instinct.",
                "The realtor shows them to the master bedroom. They have looked delighted this whole time. Why don’t you show them?",
                "What would you like to do?",
                "You try to flicker the lights. It may have worked this time, but it wasn’t really noticeable in the daylight.",
                "You try to knock over a lamp. You just barely manage to move it, but it doesn’t fall. The Smiths missed it too.",
                "You walk around looking for a creaking floorboard. You don’t seem to find one.",
                "The realtor shows the Smiths to the nursery. You have to focus and try harder. You’ve got this.",
                "What would you like to do?",
                "You reach up and try to rattle the light fixture. It swings side to side slightly. It worked! Mrs. Smith looks upwards. She doesn’t admit it, but she’s spooked.",
                "You push on the rocking horse and it actually moves. It worked! Mr. Smith turns and looks suspiciously at the creaking, rocking horse swaying slightly back and forth.",
                "You knock over the doll on the shelf. Why is it so creepy? It falls over. The youngest child turns and looks at the doll anxiously.",
                "She hardly touches the window and it falls shut suddenly, with a loud crash. After another, longer silence, she leads them out of the room as she talks about the other bedrooms that she’s going to show them.",
                "Don’t stop now! You follow them out into the hallway.",
                "What else would you like to do?",
                "The Smiths have barely made it to the next room when you start to close the nursery door behind you. It doesn’t close all the way, but it makes a creaking sound that doesn’t go unnoticed. “That’s strange, I’m sure I closed that window…” the realtor says. Then they continue to the next bedroom.",
                "You tap some of the buttons on the security alarm touchpad. It makes some beeping sounds, but the alarm doesn’t go off. The family turns to look for the source of the beeping. The realtor reminds them of security system and emphasizes what a great feature that is, but they don’t find it reassuring.",
                "Just as the realtor walks over a small rug on the hallway floor, you try to pull it out from under her. She trips, but it’s nothing serious. She brushes herself off, embarrassed, and although she doesn’t know it was you who did that, she almost appears personally upset with you. Then she turns and continues the tour.",
                "After the Smiths finish looking at the upstairs rooms, they head back downstairs. They don’t seem particularly spooked, but you definitely made them uncomfortable and they don’t seem as delighted with the house anymore. It looks like that’s the end of that."]

uglyPlayerArray = ["Flicker the lights", "Knock something over", "Make a spooky sound", "Rattle the light fixture", "Rock the rocking horse", "Move the creepy doll", "Close the door behind you", "Set off the security alarm", "Pull the rug out from the realtor"]

class PlayerDecoder(json.JSONEncoder):
    def default(self, obj):
        # pylint: disable=E0202
        # ^^ my linter does not like me overriding this
        # encoder so that comment actually does something

        # If it's a Player object it returns a dictionary with
        # relevant data
        if (isinstance(obj, Player.Player)):
            return {
                "__player__": True,
                "user_id": obj.user_id,
                "progress": obj.progress,
                "temperment": obj.temperment
            }
        else:
            return json.JSONEncoder.default(self, obj)    

# Helper class to load our JSON files
def get(file):
    try:
        with open(file, 'r', encoding='utf8') as data:
            return json.load(data)
    except AttributeError:
        raise AttributeError("Unknown argument")
    except FileNotFoundError:
        raise FileNotFoundError(f"1a JSON file {file} wasn't found")

# Same function but this parses our player database into 
# "Player" python objects
def get_player_db(file):
    try:
        with open(file, encoding='utf8') as data:
            return json.load(data, object_hook=Player.encode_player)
    except AttributeError:
        raise AttributeError("Unknown argument")
    except FileNotFoundError:
        raise FileNotFoundError(f"1b JSON file {file} was not found")


def put_player_db(data, file):
    try:
        player_dict = dict(data)
        with open(file, 'w', encoding='utf8') as player_data:
            json.dump(player_dict, player_data, cls=PlayerDecoder)
    except AttributeError:
        raise AttributeError("Unkown argument in put_player_db")
    except FileNotFoundError:
        raise FileNotFoundError(f"2b JSON file {file} not found")


# Parse the json config file
config = get("game_config.json")
db = get_player_db("db.json")

# Create Bot
bot = discord.Client()
manager = GM.GM(bot, config, db)
perms = servermanager.ServerManager(bot)
holder = IHoldThings()

@bot.event
async def on_ready():
        print(type(manager.client))
        holder.messMan = messagemanager.MessageManager(bot)
        # A list of all servers the bot is a part of
        manager.joined_servers = manager.client.servers

        # This loops checks every member it sees in 
        # every server. First it checks if the member
        # user id is in the owners list in the config
        # then to see if the user exists in our database
        # and if they don't creates a new player for them 
        # and adds it to the list
        for server in manager.joined_servers:                    
            print("list of member ids:")
            for memb in server.members:
                print(memb.id)

                if (memb.id in manager.config['owners']):
                    print(f"{memb.name} is an owner and will be assigned admin role")
                elif (memb.id in manager.players):
                    print(f"{memb.name} is already in the database")
                else:
                    print(f"{memb.name} is a new player. Adding now.")
                    new_player = Player.Player(memb.id)
                    manager.players[memb.id] = new_player.serialize_player()
                    print("Player added to self.players")
                    

        print("Updating database")
        put_player_db(manager.players, manager._db_path)
        emb = (discord.Embed(description="Press the ghost to play!", colour = 0x3DF270))
        channel = None
        for channels in bot.get_all_channels():
            if channels.id == "521107232868532254":
                channel = channels
                break
        msg = await bot.send_message(channel, embed=emb)
        await bot.add_reaction(msg, '👻')

@bot.event
async def on_message(message):
    counter = 0
    if message.content == "help":
        for elem in manager.bot_text:
            print(str(counter) + " " + elem)
            counter += 1
    if message.content == "pls":
        for elem in manager.player_text:
            print(str(counter) + " " + elem)
            counter += 1
    if message.content == "fuck":
        for elem in uglyBotArray:
            print(str(counter) + " " + elem)
            counter += 1
    if message.content == "shit":
        for elem in manager.player_text1:
            print(str(counter) + " " + elem)
            counter += 1   

@bot.event
async def on_reaction_add(reaction, user):

    if holder.scene == 1:

        if reaction.emoji == '👻' and reaction.count > 1:
            holder.messMan = messagemanager.MessageManager(bot)
            holder.currentServer = reaction.message.server
            holder.player = user
            await bot.delete_message(reaction.message)
            await perms.serverSetup(user)
            await prelude()

        if (reaction.emoji == '😐' or reaction.emoji == '😕' or reaction.emoji == '🤔') and reaction.count > 1:
            holder.currentServer = reaction.message.server
            await bot.delete_message(reaction.message)
            newMessage = ""
            if reaction.emoji == '😐':
                newMessage = "😐 "  + manager.player_text[0]
            elif reaction.emoji == '😕':
                newMessage = "😕 " + manager.player_text[1]
            else:
                newMessage = "🤔 " + manager.player_text[2]
            msg = await bot.send_message(reaction.message.channel, newMessage)
            await holder.messMan.enqueue(msg, msg.server)      
            await game_loop1()

        elif (reaction.emoji == '😓' or reaction.emoji == '😤' or reaction.emoji == '😠') and reaction.count > 1:
            holder.currentServer = reaction.message.server
            await bot.delete_message(reaction.message)
            newMessage = ""
            if reaction.emoji == '😓':
                newMessage = "😓 "  + manager.player_text[3]
            elif reaction.emoji == '😤':
                newMessage = "😤 " + manager.player_text[4]
            else:
                newMessage = "😠 " + manager.player_text[5]
            msg = await bot.send_message(reaction.message.channel, newMessage)
            await holder.messMan.enqueue(msg, msg.server)  
            await game_loop2()

        elif (reaction.emoji == '🙁' or reaction.emoji == '😧' or reaction.emoji == '😩') and reaction.count > 1:
            holder.currentServer = reaction.message.server
            await bot.delete_message(reaction.message)
            newMessage = ""
            botMesage = ""
            if reaction.emoji == '🙁':
                newMessage = "🙁 "  + manager.player_text[6]
                botMessage = manager.bot_text[11]
            elif reaction.emoji == '😧':
                newMessage = "😧 " + manager.player_text[7]
                botMessage = manager.bot_text[12]
            else:
                newMessage = "😩 " + manager.player_text[8]
                botMessage = manager.bot_text[13]
            msg = await bot.send_message(reaction.message.channel, newMessage)
            await holder.messMan.enqueue(msg, msg.server)
            botmsg = await bot.send_message(reaction.message.channel, botMessage)
            await holder.messMan.enqueue(botmsg, msg.server)
            time.sleep(5)
            await game_loop3()

        elif (reaction.emoji == '💡' or reaction.emoji == '💥' or reaction.emoji == '🚪') and reaction.count > 1:
            holder.currentServer = reaction.message.server
            await bot.delete_message(reaction.message)
            newMessage = ""
            botMessage = ""
            if reaction.emoji == '💡':
                newMessage = "💡 "  + manager.player_text[9]
                botMessage = manager.bot_text[16]
            elif reaction.emoji == '💥':
                newMessage = "💥 " + manager.player_text[10]
                botMessage = manager.bot_text[17]
            else:
                newMessage = "🚪 " + manager.player_text[11]
                botMessage = manager.bot_text[18]
            msg = await bot.send_message(reaction.message.channel, newMessage)
            await holder.messMan.enqueue(msg, msg.server)
            botmsg = await bot.send_message(reaction.message.channel, botMessage)
            await holder.messMan.enqueue(botmsg, msg.server)
            time.sleep(5)
            await game_loop4()

        elif (reaction.emoji == '💺' or reaction.emoji == '💨' or reaction.emoji == '🔑') and reaction.count > 1:
            holder.currentServer = reaction.message.server
            await bot.delete_message(reaction.message)
            newMessage = ""
            botMessage = ""
            if reaction.emoji == '💺':
                newMessage = "💺 "  + manager.player_text[12]
                botMessage = manager.bot_text[20]
            elif reaction.emoji == '💨':
                newMessage = "💨 " + manager.player_text[13]
                botMessage = manager.bot_text[21]
            else:
                newMessage = "🔑 " + manager.player_text[14]
                botMessage = manager.bot_text[22]
            msg = await bot.send_message(reaction.message.channel, newMessage)
            await holder.messMan.enqueue(msg, msg.server)
            botmsg = await bot.send_message(reaction.message.channel, botMessage)
            await holder.messMan.enqueue(botmsg, msg.server)
            time.sleep(5)
            await game_loop5()

        elif (reaction.emoji == '😑' or reaction.emoji == '😞' or reaction.emoji == '🙄') and reaction.count > 1:
            holder.currentServer = reaction.message.server
            await bot.delete_message(reaction.message)
            newMessage = ""
            botMessage = ""
            if reaction.emoji == '😑':
                newMessage = "😑 "  + manager.player_text[15]
                botMessage = manager.bot_text[24]
            elif reaction.emoji == '😞':
                newMessage = "😞 " + manager.player_text[16]
                botMessage = manager.bot_text[25]
            else:
                newMessage = "🙄 " + manager.player_text[17]
                botMessage = manager.bot_text[26]
            msg = await bot.send_message(reaction.message.channel, newMessage)
            await holder.messMan.enqueue(msg, msg.server)  
            await game_loop6()

    if holder.scene == 2:

        if (reaction.emoji == '💡' or reaction.emoji == '💥' or reaction.emoji == '👻') and reaction.count > 1:
            holder.currentServer = reaction.message.server
            await bot.delete_message(reaction.message)
            newMessage = ""
            botMessage = ""
            if reaction.emoji == '💡':
                newMessage = "💡 "  + uglyPlayerArray[0]
                botMessage = uglyBotArray[3]
            elif reaction.emoji == '💥':
                newMessage = "💥 " + uglyPlayerArray[1]
                botMessage = uglyBotArray[4]
            else:
                newMessage = "👻 " + uglyPlayerArray[2]
                botMessage = uglyBotArray[5]
            msg = await bot.send_message(reaction.message.channel, newMessage)
            await holder.messMan.enqueue(msg, msg.server)  
            await game_loop7()


        elif (reaction.emoji == '😠' or reaction.emoji == '🐎' or reaction.emoji == '👧') and reaction.count > 1:
            holder.currentServer = reaction.message.server
            await bot.delete_message(reaction.message)
            newMessage = ""
            botMessage = ""
            if reaction.emoji == '😠':
                newMessage = "😠 "  + uglyPlayerArray[3]
                botMessage = uglyBotArray[8]
            elif reaction.emoji == '🐎':
                newMessage = "🐎 " + uglyPlayerArray[4]
                botMessage = uglyBotArray[9]
            else:
                newMessage = "👧 " + uglyPlayerArray[5]
                botMessage = uglyBotArray[10]
            msg = await bot.send_message(reaction.message.channel, newMessage)
            await holder.messMan.enqueue(msg, msg.server)  
            await game_loop8()
        



@bot.event
async def prelude():
    time.sleep(2)
    channel = await perms.getChannelByName("aether", holder.currentServer)
    emb = (discord.Embed(description="A swirling vortex of purple mist greets your eyes...", colour = 0x3DF270))
    emb.set_image(url = "https://cdn.discordapp.com/attachments/520071023144599569/521500561279811597/aether2.jpg")
    await bot.send_message(channel, embed=emb) 
    msg = await bot.send_message(channel, "....What is all this purple stuff?")
    await holder.messMan.enqueue(msg, msg.server)
    time.sleep(5)
    channel = await perms.getChannelByName("aether", holder.currentServer)
    msg = await bot.send_message(channel, "This dream is fucking weird.")
    await holder.messMan.enqueue(msg, msg.server)
    time.sleep(5)
    await perms.grantPermissions(holder.player, "attic")
    msg = await bot.send_message(channel, "#attic")
    await game_loop()

@bot.event
async def game_loop():
    time.sleep(2)
    channel = await perms.getChannelByName("attic", holder.currentServer)  
    emb = (discord.Embed(description="My attic... but something seems off", colour = 0x3DF270))
    emb.set_image(url = "https://cdn.discordapp.com/attachments/518583486672535565/520023726742437888/attic.jpg")
    await bot.send_message(channel, embed=emb)

    botsTurn = True

    while botsTurn:
        msg = await bot.send_message(channel, manager.bot_text[holder.botprogress])
        await holder.messMan.enqueue(msg, msg.server)
        time.sleep(5)
        holder.botprogress += 1
        if holder.botprogress == 4:
            botsTurn = False

    emojis = ['😐', '😕', '🤔']
    channel = await perms.getChannelByName("attic", holder.currentServer)
    nextChoices = emojis[0] + ": " + manager.player_text[holder.progress] + "\n"
    holder.progress += 1
    nextChoices += emojis[1] + ": " + manager.player_text[holder.progress] + "\n"
    holder.progress += 1
    nextChoices += emojis[2] + ": " + manager.player_text[holder.progress] + "\n"
    holder.progress += 1
    emb = (discord.Embed(description=nextChoices, colour = 0x3DF270))
    msg = await bot.send_message(channel, embed=emb)
    for emoji in emojis:
        await bot.add_reaction(msg, emoji)
    time.sleep(2)

    


@bot.event
async def game_loop1():
    botsTurn = True

    while botsTurn:
        channel = await perms.getChannelByName("attic", holder.currentServer)
        msg = await bot.send_message(channel, manager.bot_text[holder.botprogress])
        await holder.messMan.enqueue(msg, msg.server)
        time.sleep(5)
        holder.botprogress += 1
        if holder.botprogress == 6:
            botsTurn = False

    emojis = ['😓', '😤', '😠']
    channel = await perms.getChannelByName("attic", holder.currentServer)
    nextChoices = emojis[0] + ": " + manager.player_text[holder.progress] + "\n"
    holder.progress += 1
    nextChoices += emojis[1] + ": " + manager.player_text[holder.progress] + "\n"
    holder.progress += 1
    nextChoices += emojis[2] + ": " + manager.player_text[holder.progress] + "\n"
    holder.progress += 1
    emb = (discord.Embed(description=nextChoices, colour = 0x3DF270))
    msg = await bot.send_message(channel, embed=emb)
    for emoji in emojis:
        await bot.add_reaction(msg, emoji)
    time.sleep(2)

@bot.event
async def game_loop2():
    botsTurn = True

    while botsTurn:
        channel = await perms.getChannelByName("attic", holder.currentServer)
        msg = await bot.send_message(channel, manager.bot_text[holder.botprogress])
        await holder.messMan.enqueue(msg, msg.server)
        time.sleep(5)
        holder.botprogress += 1
        if holder.botprogress == 11:
            botsTurn = False

    emojis = ['🙁', '😧', '😩']
    channel = await perms.getChannelByName("attic", holder.currentServer)
    nextChoices = emojis[0] + ": " + manager.player_text[holder.progress] + "\n"
    holder.progress += 1
    nextChoices += emojis[1] + ": " + manager.player_text[holder.progress] + "\n"
    holder.progress += 1
    nextChoices += emojis[2] + ": " + manager.player_text[holder.progress] + "\n"
    holder.progress += 1
    emb = (discord.Embed(description=nextChoices, colour = 0x3DF270))
    msg = await bot.send_message(channel, embed=emb)
    for emoji in emojis:
        await bot.add_reaction(msg, emoji)
    time.sleep(2)


@bot.event
async def game_loop3():
    channel = await perms.getChannelByName("attic", holder.currentServer)
    msg = await bot.send_message(channel, manager.bot_text[14])
    await holder.messMan.enqueue(msg, msg.server)
    time.sleep(5)
    msg = await bot.send_message(channel, manager.bot_text[15])
    await holder.messMan.enqueue(msg, msg.server)
    time.sleep(5)


    emojis = ['💡', '💥', '🚪']
    channel = await perms.getChannelByName("attic", holder.currentServer)
    nextChoices = emojis[0] + ": " + manager.player_text[holder.progress] + "\n"
    holder.progress += 1
    nextChoices += emojis[1] + ": " + manager.player_text[holder.progress] + "\n"
    holder.progress += 1
    nextChoices += emojis[2] + ": " + manager.player_text[holder.progress] + "\n"
    holder.progress += 1
    emb = (discord.Embed(description=nextChoices, colour = 0x3DF270))
    msg = await bot.send_message(channel, embed=emb)
    for emoji in emojis:
        await bot.add_reaction(msg, emoji)
    time.sleep(2)

@bot.event
async def game_loop4():
    channel = await perms.getChannelByName("attic", holder.currentServer)
    msg = await bot.send_message(channel, manager.bot_text[19])
    await holder.messMan.enqueue(msg, msg.server)
    time.sleep(5)


    emojis = ['💺', '💨', '🔑']
    channel = await perms.getChannelByName("attic", holder.currentServer)
    nextChoices = emojis[0] + ": " + manager.player_text[holder.progress] + "\n"
    holder.progress += 1
    nextChoices += emojis[1] + ": " + manager.player_text[holder.progress] + "\n"
    holder.progress += 1
    nextChoices += emojis[2] + ": " + manager.player_text[holder.progress] + "\n"
    holder.progress += 1
    emb = (discord.Embed(description=nextChoices, colour = 0x3DF270))
    msg = await bot.send_message(channel, embed=emb)
    for emoji in emojis:
        await bot.add_reaction(msg, emoji)
    time.sleep(2)

@bot.event
async def game_loop5():
    channel = await perms.getChannelByName("attic", holder.currentServer)
    msg = await bot.send_message(channel, manager.bot_text[23])
    await holder.messMan.enqueue(msg, msg.server)
    time.sleep(5)

    emojis = ['😑', '😞', '🙄']
    channel = await perms.getChannelByName("attic", holder.currentServer)
    nextChoices = emojis[0] + ": " + manager.player_text[holder.progress] + "\n"
    holder.progress += 1
    nextChoices += emojis[1] + ": " + manager.player_text[holder.progress] + "\n"
    holder.progress += 1
    nextChoices += emojis[2] + ": " + manager.player_text[holder.progress] + "\n"
    holder.progress += 1
    emb = (discord.Embed(description=nextChoices, colour = 0x3DF270))
    msg = await bot.send_message(channel, embed=emb)
    for emoji in emojis:
        await bot.add_reaction(msg, emoji)
    time.sleep(2)

@bot.event
async def game_loop6():
    channel = await perms.getChannelByName("attic", holder.currentServer)
    msg = await bot.send_message(channel, manager.bot_text[27])
    await holder.messMan.enqueue(msg, msg.server)
    time.sleep(5)
    msg = await bot.send_message(channel, manager.bot_text[28])
    await holder.messMan.enqueue(msg, msg.server)
    time.sleep(5)
    msg = await bot.send_message(channel, manager.bot_text[29])
    await holder.messMan.enqueue(msg, msg.server)
    time.sleep(5)
    holder.scene = 2
    await perms.grantPermissions(holder.player, "masterbedroom")
    msg = await bot.send_message(channel, "#masterbedroom")
    await holder.messMan.enqueue(msg, msg.server)


    channel = await perms.getChannelByName("masterbedroom", holder.currentServer)
    time.sleep(2)
    emb = (discord.Embed(description="My bedroom, but much nicer than how I left it.", colour = 0x3DF270))
    emb.set_image(url = "https://cdn.discordapp.com/attachments/520071023144599569/523040030533615616/masterbed.jpg")
    await bot.send_message(channel, embed=emb)
    msg = await bot.send_message(channel, uglyBotArray[0])
    await holder.messMan.enqueue(msg, msg.server)
    time.sleep(5)
    msg = await bot.send_message(channel, uglyBotArray[1])
    await holder.messMan.enqueue(msg, msg.server)
    time.sleep(5)
    msg = await bot.send_message(channel, uglyBotArray[2])
    await holder.messMan.enqueue(msg, msg.server)
    time.sleep(5)

    emojis = ['💡', '💥', '👻']
    channel = await perms.getChannelByName("masterbedroom", holder.currentServer)
    nextChoices = emojis[0] + ": " + uglyPlayerArray[0] + "\n"
    nextChoices += emojis[1] + ": " + uglyPlayerArray[1] + "\n"
    nextChoices += emojis[2] + ": " + uglyPlayerArray[2] + "\n"
    emb = (discord.Embed(description=nextChoices, colour = 0x3DF270))
    msg = await bot.send_message(channel, embed=emb)
    for emoji in emojis:
        await bot.add_reaction(msg, emoji)
    time.sleep(2)

@bot.event
async def game_loop7():
    channel = await perms.getChannelByName("masterbedroom", holder.currentServer)
    msg = await bot.send_message(channel, uglyBotArray[6])
    await holder.messMan.enqueue(msg, msg.server)
    time.sleep(5)
    msg = await bot.send_message(channel, uglyBotArray[7])
    await holder.messMan.enqueue(msg, msg.server)
    time.sleep(5)

    emojis = ['😠', '🐎', '👧']
    nextChoices = emojis[0] + ": " + uglyPlayerArray[3] + "\n"
    holder.progress += 1
    nextChoices += emojis[1] + ": " + uglyPlayerArray[4] + "\n"
    holder.progress += 1
    nextChoices += emojis[2] + ": " + uglyPlayerArray[5] + "\n"
    holder.progress += 1
    emb = (discord.Embed(description=nextChoices, colour = 0x3DF270))
    msg = await bot.send_message(channel, embed=emb)
    for emoji in emojis:
        await bot.add_reaction(msg, emoji)
    time.sleep(2)


@bot.event
async def game_loop8():
    channel = await perms.getChannelByName("masterbedroom", holder.currentServer)
    msg = await bot.send_message(channel, uglyBotArray[11])
    await holder.messMan.enqueue(msg, msg.server)
    time.sleep(5)
    msg = await bot.send_message(channel, uglyBotArray[12])
    await holder.messMan.enqueue(msg, msg.server)
    time.sleep(5)

    emojis = ['😠', '🐎', '👧']
    nextChoices = emojis[0] + ": " + uglyPlayerArray[6] + "\n"
    holder.progress += 1
    nextChoices += emojis[1] + ": " + uglyPlayerArray[7] + "\n"
    holder.progress += 1
    nextChoices += emojis[2] + ": " + uglyPlayerArray[8] + "\n"
    holder.progress += 1
    emb = (discord.Embed(description=nextChoices, colour = 0x3DF270))
    msg = await bot.send_message(channel, embed=emb)
    for emoji in emojis:
        await bot.add_reaction(msg, emoji)
    time.sleep(2)


bot.run(config['crow_token'])
