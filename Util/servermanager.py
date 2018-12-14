import discord
from discord.ext import commands
import asyncio

#commentsarefun
class ServerManager:
    def __init__(self, client):
        self.client = client
        self.roomNames = ["aether", "attic", "hallway", "masterbedroom", "nursery", "bathroom", "hall", "kitchen", "livingroom", "diningroom", "study", "trophyroom"]

    async def serverSetup(self, member):
        playerRoleAlreadyExists = False

        for role in member.server.roles:
            if role.name == "Player":
                playerRoleAlreadyExists = True

        if(playerRoleAlreadyExists):
            role = discord.utils.get(member.server.roles, name="Player")
            await self.client.add_roles(member, role)

        else:
            await self.client.create_role(member.server, name="Player")
            role = discord.utils.get(member.server.roles, name="Player")
            await self.client.add_roles(member, role)

        toBeCreated = []

        for names in self.roomNames:
            channelExists = False
            channelArray = self.client.get_all_channels()
            for channels in channelArray:
                if channels.server == member.server:
                    if channels.name == names:
                        async for messages in self.client.logs_from(channels):
                            await self.client.delete_message(messages)
                        channelExists = True
            if channelExists == False:
                toBeCreated.append(names)


        for names in toBeCreated:
            await self.client.create_channel(member.server, names, type=discord.ChannelType.text)           

            
        for channels in self.client.get_all_channels():
            if channels.server == member.server:
                if (channels.type == discord.ChannelType.text):
                    overwrite = discord.PermissionOverwrite()
                    overwrite.send_messages = False
                    overwrite.add_reactions = False
                    if channels.name != "aether":
                        overwrite.read_messages = False
                    await self.client.edit_channel_permissions(channels, member, overwrite)



    async def grantAllPermissions(self, member):
        for channels in self.client.get_all_channels():
            if channels.server == member.server:
                if (channels.type == discord.ChannelType.text):
                    overwrite = discord.PermissionOverwrite()
                    overwrite.send_messages = True
                    overwrite.add_reactions = True
                    overwrite.read_messages = True
                    await self.client.edit_channel_permissions(channels, member, overwrite)

    async def getChannelByName(self, name, server):
        for channels in self.client.get_all_channels():
            if name == channels.name:
                if channels.server == server:
                    return channels


    async def grantPermissions(self, member, progress):
        if progress == "attic":
            channel = await self.getChannelByName(name="attic", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = True
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await self.client.edit_channel_permissions(channel, member, overwrite) 

            channel = await self.getChannelByName(name="aether", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = True
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await self.client.edit_channel_permissions(channel, member, overwrite)


        elif progress == "hallway":
            channel = await self.getChannelByName(name="hallway", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = True
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await self.client.edit_channel_permissions(channel, member, overwrite) 

            channel = await self.getChannelByName(name="masterbedroom", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = True
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await self.client.edit_channel_permissions(channel, member, overwrite)

            channel = await self.getChannelByName(name="nursery", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = True
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await self.client.edit_channel_permissions(channel, member, overwrite) 

            channel = await self.getChannelByName(name="bathroom", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = True
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await self.client.edit_channel_permissions(channel, member, overwrite)


        elif progress == "bathroom":
            channel = await self.getChannelByName(name="hallway", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = True
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await self.client.edit_channel_permissions(channel, member, overwrite) 

            channel = await self.getChannelByName(name="masterbedroom", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = False
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await self.client.edit_channel_permissions(channel, member, overwrite)

            channel = await self.getChannelByName(name="nursery", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = False
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await self.client.edit_channel_permissions(channel, member, overwrite) 

            channel = await self.getChannelByName(name="bathroom", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = True
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await self.client.edit_channel_permissions(channel, member, overwrite) 
            
            channel = await self.getChannelByName(name="attic", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = False
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await self.client.edit_channel_permissions(channel, member, overwrite)

        elif progress == "masterbedroom":
            channel = await self.getChannelByName(name="hallway", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = False
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await self.client.edit_channel_permissions(channel, member, overwrite) 

            channel = await self.getChannelByName(name="masterbedroom", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = True
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await self.client.edit_channel_permissions(channel, member, overwrite)

            channel = await self.getChannelByName(name="nursery", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = False
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await self.client.edit_channel_permissions(channel, member, overwrite) 

            channel = await self.getChannelByName(name="bathroom", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = False
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await self.client.edit_channel_permissions(channel, member, overwrite) 
            
            channel = await self.getChannelByName(name="attic", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = True
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await self.client.edit_channel_permissions(channel, member, overwrite)

            channel = await self.getChannelByName(name="aether", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = False
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await self.client.edit_channel_permissions(channel, member, overwrite)

        elif progress == "nursery":
            channel = await self.getChannelByName(name="hallway", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = True
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await self.client.edit_channel_permissions(channel, member, overwrite) 

            channel = await self.getChannelByName(name="masterbedroom", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = False
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await self.client.edit_channel_permissions(channel, member, overwrite)

            channel = await self.getChannelByName(name="nursery", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = True
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await self.client.edit_channel_permissions(channel, member, overwrite) 

            channel = await self.getChannelByName(name="bathroom", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = False
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await self.client.edit_channel_permissions(channel, member, overwrite) 
            
            channel = await self.getChannelByName(name="attic", server=member.server)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = False
            overwrite.send_messages = False
            overwrite.add_reactions = False
            await self.client.edit_channel_permissions(channel, member, overwrite) 
