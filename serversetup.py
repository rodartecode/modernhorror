import discord
from discord.ext import commands
import asyncio


client = discord.Client()

class Stats:
    roomNames = ["aether", "attic", "hallway", "masterbedroom", "nursery", "bathroom", "hallway", "kitchen", "livingroom", "diningroom", "study", "trophyroom"]

options = Stats()

#WARNING!!!!
#WARNING!!!!
#WARNING!!!!
#There is a function call in here that erases messages from every game channel. Run at your own risk!


@client.event
async def server_setup(member):
    playerRoleAlreadyExists = False


#Player role does not govern channel visibility - it's not possible to toggle channels for individual roles.
#This does assign Player, though, and will create the role if it does not already exist.

    for role in member.server.roles:
        if role.name == "Player":
            playerRoleAlreadyExists = True

    if(playerRoleAlreadyExists):
        role = discord.utils.get(member.server.roles, name="Player")
        await client.add_roles(member, role)

    else:
        await client.create_role(member.server, name="Player")
        role = discord.utils.get(member.server.roles, name="Player")
        await client.add_roles(member, role)


    print("creating channels")

#this will create channels if they do not already exist
#WARNING!!! Contains a for-loop that erases ALL messages in game channels!
    for names in options.roomNames:
        channelExists = False
        channelArray = client.get_all_channels()
        for channels in channelArray:
            print("name: " + names + "   channel: " + channels.name)
            if channels.name == names:
                async for messages in client.logs_from(channels):
                    await client.delete_message(messages)
                channelExists = True
        if channelExists == False:
                print(names + " doesn't exist, creating")
                await client.create_channel(member.server, names, type=discord.ChannelType.text)           

        
#makes channels invisible to the player. unfortunately, this is member specific and cannot be adjusted by role.
#does not hide the "aether" channel as that's where the game starts.
    print("hiding channels")
    for channels in client.get_all_channels():
        if channels.server == member.server:
            if (channels.type == discord.ChannelType.text):
                print("in channel: " + channels.name)
                overwrite = discord.PermissionOverwrite()
                overwrite.send_messages = False
                overwrite.add_reactions = False
                if channels.name != "aether":
                    overwrite.read_messages = False
                await client.edit_channel_permissions(channels, member, overwrite)

#populates every game channel with an embed. A string array can handle the urls
    print("setting up channels")
    for channels in client.get_all_channels():
        if channels.server == member.server:
            isPartOfGame = False
            for names in options.roomNames:
                if names == channels.name:
                    isPartOfGame = True
            if isPartOfGame:
                emb = (discord.Embed(description="text here", colour = 0x3DF270))
                emb.set_image(url = "https://i.ytimg.com/vi/EjLqKt9JNlA/maxresdefault.jpg")
                await client.send_message(channels, embed=emb)

#returns a channel based on given name.
@client.event
async def getChannelByName(name):
    for channels in client.get_all_channels():
        if name == channels.name:
            return channels