import discord
from discord.ext import commands

import os
import xml.etree.ElementTree as et

#XMl Parsing stuff here??

TOKEN = ''

client = commands.Bot(command_prefix = '!')

class EmbedTemplate:
    pass


@client.event
async def on_ready():
    print('Bot is ready.')


#Exposition Embed - embed template for scene-setting bits of text
@client.command()  # ?? Will this be a command or an event?
async def displayExpoEmbed ():
    xml_title =  '' #Get scene title from XML
    xml_description = '' #Get scene description from XMl
    expoEmbed = discord.Embed(
        title = xml_title,
        description = xml_description,
        color = discord.Colour.default()
    )

    expoEmbed.set_author(name = '') # ?? Should this be set to the MasterBot's name? The level/room name? Or left blank?
    await client.say(embed = expoEmbed)

#Prompt Embed - embed template for prompts
#(where the bot will display the different actions a user can take, and the corresponding emojis)
@client.command() # ?? Will this be a command or an event?
async def displayPromptEmbed ():
    xml_title = '' #Get scene title from XML
    promptEmbed = discord.Embed(
        title = xml_title,
        description = 'Choose what action you will take', #Not sold on this wording, open to suggestions
        color = discord.Color.green()
    )
    promptEmbed.set_author(name = '') # ?? Should this be set to the MasterBot's name? The level/room name? Or left blank?

    #Use a number add_field()s as needed depending on the available actions the user needs to take
    #Perhaps in a for loop??
    #Perhaps name='~emoji~' and value='~action description~'
    promptEmbed.add_field(name='', value='', inline=False)
    await client.say(embed = promptEmbed)

#Response Embed - embed template for the bot's response to the user's actions
@client.command() # ?? Will this be a command or an event?
async def displayResponseEmbed ():
    xml_title = '' #Get scene title from XML
    xml_description = '' #Pull response from XMl based on corresponding action selected by user in the promptEmbed
    responseEmbed = discord.Embed(
        title = xml_title, # Scene title pulled from XML
        description = xml_description,
        color = discord.Color.blue()
    )

    await client.say(embed = responseEmbed)

client.run(TOKEN)
