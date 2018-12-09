import discord
from discord.ext import commands
import asyncio


client = discord.Client()


class Stats:
    roomNames = ["aether", "attic", "hallway", "masterbedroom", "nursery", "bathroom", "hallway", "kitchen", "livingroom", "diningroom", "study", "trophyroom"]


options = Stats()


#A very basic queue class. It is reversed in order (0 is the back, not the front)

class Queue:
    def __init__(self):
        self.items = []
    async def enqueue(self, item):
        self.items.insert(0, item)
    async def dequeue(self):
        return self.items.pop()
    async def size(self):
        return len(self.items)

#Message Manager stores an array of 12 queues (one for each room). Once instantiated, the member function .enqueue(message) can be called
#in on_message as messagemanager.enqueue(message) to automatically put the message into the right queue. the roomNames
#array is used to determine the index of the queue array. The enqueue function ignores embeds.

class MessageManager:
    def __init__(self):
        self.messageQueue = [Queue() for i in range(12)]
  
    async def enqueue(self, message):
        if message.content == "":
            return
        else:
            if await self.messageQueue[options.roomNames.index(message.channel.name)].size() < 9:
                print("enqueueing: " + message.content + " in channel " + message.channel.name)
                await self.messageQueue[options.roomNames.index(message.channel.name)].enqueue(message)
            else:
                msg = await self.messageQueue[options.roomNames.index(message.channel.name)].dequeue()
                print("dequeueing: " + msg.content + " in channel " + msg.channel.name)
                await client.delete_message(msg)
                await self.messageQueue[options.roomNames.index(message.channel.name)].enqueue(message)
                print("enqueueing: " + message.content + " in channel " + message.channel.name)