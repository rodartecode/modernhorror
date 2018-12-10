import discord
from discord.ext import commands
import asyncio

client = discord.Client()

#updated with a clear function.
class Queue:
    def __init__(self):
        self.items = []
    async def enqueue(self, item):
        self.items.insert(0, item)
    async def dequeue(self):
        return self.items.pop()
    async def size(self):
        return len(self.items)
    async def clear(self):
        while await self.size() > 0:
            self.items.pop()


class MessageManager:
    def __init__(self):
        self.roomNames = ["aether", "attic", "hallway", "masterbedroom", "nursery", "bathroom", "hall", "kitchen", "livingroom", "diningroom", "study", "trophyroom"]
        self.messageQueue = [Queue() for i in range(12)]
  

    async def enqueue(self, message, server):
        #this if statement allows MessageManager to ignore embeds, regardless of content.
        if message.content == "":
                return
        for names in self.roomNames:
            if message.channel.name == names:
                if message.server == server:
                    if await self.messageQueue[self.roomNames.index(message.channel.name)].size() < 9:
                        print("enqueueing: " + message.content + " in channel " + message.channel.name)
                        await self.messageQueue[self.roomNames.index(message.channel.name)].enqueue(message)
                        return
                    else:
                        msg = await self.messageQueue[self.roomNames.index(message.channel.name)].dequeue()
                        print("dequeueing: " + msg.content + " in channel " + msg.channel.name)
                        await client.delete_message(msg)
                        await self.messageQueue[self.roomNames.index(message.channel.name)].enqueue(message)
                        print("enqueueing: " + message.content + " in channel " + message.channel.name)
                        return



