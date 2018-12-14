import discord
from discord.ext import commands
import asyncio


#updated with a clear function.
class Queue:
    def __init__(self):
        self.items = []
        self.count = 0
    async def enqueue(self, item):
        self.count += 1
        self.items.insert(0, item)
    async def dequeue(self):
        self.count -= 1
        return self.items.pop()
    async def size(self):
        return len(self.items)
    async def clear(self):
        while await self.size() > 0:
            self.items.pop()


class MessageManager:
    def __init__(self, bot):
        self.bot = bot
        self.roomNames = ["aether", "attic", "hallway", "masterbedroom", "nursery", "bathroom", "hall", "kitchen", "livingroom", "diningroom", "study", "trophyroom"]
        self.messageQueue = [Queue() for i in range(12)]
  

    async def enqueue(self, message, server):
        for names in self.roomNames:
            if message.channel.name == names:
                if message.server == server:
                    if self.messageQueue[self.roomNames.index(message.channel.name)].count >= 5:
                        print("in dequeue")
                        msg = await self.messageQueue[self.roomNames.index(message.channel.name)].dequeue()
                        print(msg.content)
                        await self.bot.delete_message(msg)
                    print("enqueueing: " + message.content + " in channel " + message.channel.name)
                    await self.messageQueue[self.roomNames.index(message.channel.name)].enqueue(message)

    async def clear(self, channel):
        self.messageQueue[self.roomNames.index(channel)].clear()
                        


