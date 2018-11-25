import asyncio
import discord
import disc_config as cfg
import Casper
from collections import namedtuple


CASPER_TOKEN = cfg.disc_token

# First, we must attach an event signalling when the bot has been
# closed to the client itself so we know when to fully close the event loop.

Entry = namedtuple('Entry', 'client event')
entries = [
  Entry(client=discord.Client(), event=asyncio.Event())
]

# Then, we should login to all our clients and wrap the connect call
# so it knows when to do the actual full closure

loop = asyncio.get_event_loop()

loop.create_task(Casper.start(CASPER_TOKEN))


async def login():
  for e in entries:
    await e.client.login()

async def wrapped_connect(entry):
  try:
    await entry.client.connect()
  except Exception as e:
    await entry.client.close()
    print('We got an exception: ', e.__class__.__name__, e)
    entry.event.set()

# actually check if we should close the event loop:
async def check_close():
  futures = [e.event.wait() for e in entries]
  await asyncio.wait(futures)

# here is when we actually login
loop.run_until_complete(login())

# now we connect to every client
for entry in entries:
  loop.create_task(wrapped_connect(entry))

# now we're waiting for all the clients to close
loop.run_until_complete(check_close())

# finally, we close the event loop
loop.close()