import discord
from discord.ext import commands
import asyncio


client = discord.Client()

class ServerManager:
    #the string array is necessary to leave non-game channels unaffected by the message clearing function
    def __init__(self):
        self.bot = bot
        self.roomNames = ["aether", "attic", "hallway", "masterbedroom", "nursery", "bathroom", "hall", "kitchen", "livingroom", "diningroom", "study", "trophyroom"]


    @commands.command()
    async def serverSetup(self, member):
        playerRoleAlreadyExists = False

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


        #this function will create any missing channels, please note, the for loop on line 40 will delete ALL messages from existing game channels.
        for names in self.roomNames:
            channelExists = False
            channelArray = client.get_all_channels()
            for channels in channelArray:
                if channels.server == member.server:
                    if channels.name == names:
                        async for messages in client.logs_from(channels):
                            await client.delete_message(messages)
                        channelExists = True
            if channelExists == False:
                    await client.create_channel(member.server, names, type=discord.ChannelType.text)           


        #removes write and reaction permissions for all channels, and read permissions for all channels except for aether. this INCLUDES non-game channels.    
        #to only remove permissions for game channels, add:
        #for names in self.roomNames:
        #   if channels.name == names:
        #to line 54 and indent the rest once
        for channels in client.get_all_channels():
            if channels.server == member.server:
                if (channels.type == discord.ChannelType.text):
                    overwrite = discord.PermissionOverwrite()
                    overwrite.send_messages = False
                    overwrite.add_reactions = False
                    if channels.name != "aether":
                        overwrite.read_messages = False
                    await client.edit_channel_permissions(channels, member, overwrite)


        #populates each game channel with an exposition - this works but has issues.
        for channels in client.get_all_channels():
            if channels.server == member.server:
                isPartOfGame = False
                for names in self.roomNames:
                    if names == channels.name:
                        isPartOfGame = True
                if isPartOfGame:
                    emb = (discord.Embed(description="text here", colour = 0x3DF270))
                    if channels.name == "aether":
                        emb.set_image(url = "https://cdn.discordapp.com/attachments/520071023144599569/521500561279811597/aether2.jpg")
                    elif channels.name == "attic":
                        emb.set_image(url = "https://cdn.discordapp.com/attachments/518583486672535565/520023726742437888/attic.jpg")
                    else:                 
                        emb.set_image(url = "https://i.ytimg.com/vi/EjLqKt9JNlA/maxresdefault.jpg")
                    msg = await client.send_message(channels, embed=emb)



    #pass in a Member to grant full permissions to all channels in the server to that member.
    @commands.command()
    async def grantAllPermissions(self, member):
        for channels in client.get_all_channels():
            if channels.server == member.server:
                if (channels.type == discord.ChannelType.text):
                    overwrite = discord.PermissionOverwrite()
                    overwrite.send_messages = True
                    overwrite.add_reactions = True
                    overwrite.read_messages = True
                    await client.edit_channel_permissions(channels, member, overwrite)



    #pass in a String as the name argument and a server for the server argument to receive a Channel object
    #the server argument is necessary because the bot can see all channels with the given name,
    #so if there is a second server with that same channel name, it can return a channel in the wrong server.
    @commands.command()
    async def getChannelByName(self, name, server):
        for channels in client.get_all_channels():
            if channels.server == server:
                if name == channels.name:
                    return channels


    #takes a Member and grants permissions based on what they should see in real life if they were in a room!
    #progress is a string but can be changed to an int. ALL permissions must be decided when creating a PermissionOverwrite object.
    #This is because PermissionOverwrite contains default values and, well, overwrites all permissions for a given member!
    #Please note this function will be updated to call a new function not yet added to add an exposition to a channel when visited
    #for the first time. It must be done this way because Discord uses a timed sync to check for permissions in a given server -
    #meaning, in short, that messages posted while read permissions were not granted will become visible *eventually* but not immediately.
    @commands.command()
    async def grantPermissions(self, member, progress):
        if progress == "attic":
            channel = await self.getChannelByName(name="attic", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = True
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await client.edit_channel_permissions(channel, member, overwrite) 

            channel = await self.getChannelByName(name="aether", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = False
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await client.edit_channel_permissions(channel, member, overwrite)


        elif progress == "hallway":
            channel = await self.getChannelByName(name="hallway", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = True
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await client.edit_channel_permissions(channel, member, overwrite) 

            channel = await self.getChannelByName(name="masterbedroom", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = True
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await client.edit_channel_permissions(channel, member, overwrite)

            channel = await self.getChannelByName(name="nursery", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = True
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await client.edit_channel_permissions(channel, member, overwrite) 

            channel = await self.getChannelByName(name="bathroom", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = True
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await client.edit_channel_permissions(channel, member, overwrite)


        elif progress == "bathroom":
            channel = await self.getChannelByName(name="hallway", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = True
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await client.edit_channel_permissions(channel, member, overwrite) 

            channel = await self.getChannelByName(name="masterbedroom", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = False
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await client.edit_channel_permissions(channel, member, overwrite)

            channel = await self.getChannelByName(name="nursery", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = False
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await client.edit_channel_permissions(channel, member, overwrite) 

            channel = await self.getChannelByName(name="bathroom", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = True
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await client.edit_channel_permissions(channel, member, overwrite) 
            
            channel = await self.getChannelByName(name="attic", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = False
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await client.edit_channel_permissions(channel, member, overwrite)

        elif progress == "masterbedroom":
            channel = await self.getChannelByName(name="hallway", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = True
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await client.edit_channel_permissions(channel, member, overwrite) 

            channel = await self.getChannelByName(name="masterbedroom", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = True
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await client.edit_channel_permissions(channel, member, overwrite)

            channel = await self.getChannelByName(name="nursery", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = False
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await client.edit_channel_permissions(channel, member, overwrite) 

            channel = await self.getChannelByName(name="bathroom", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = False
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await client.edit_channel_permissions(channel, member, overwrite) 
            
            channel = await self.getChannelByName(name="attic", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = False
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await client.edit_channel_permissions(channel, member, overwrite)

        elif progress == "nursery":
            channel = await self.getChannelByName(name="hallway", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = True
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await client.edit_channel_permissions(channel, member, overwrite) 

            channel = await self.getChannelByName(name="masterbedroom", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = False
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await client.edit_channel_permissions(channel, member, overwrite)

            channel = await self.getChannelByName(name="nursery", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = True
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await client.edit_channel_permissions(channel, member, overwrite) 

            channel = await self.getChannelByName(name="bathroom", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = False
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await client.edit_channel_permissions(channel, member, overwrite) 
            
            channel = await self.getChannelByName(name="attic", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = False
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await client.edit_channel_permissions(channel, member, overwrite) 

def setup(bot):
    bot.add_cog(Members(bot))