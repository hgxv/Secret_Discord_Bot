import discord
import asyncio

from config import TOKEN, CHANNEL, ADMIN_ID, IS_EVENT_ON
from commands import (
    Register_event,
    reveal,
    voters,
    secrets,
    available,
    start_event,
)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")
    client.channel = client.get_channel(CHANNEL)
    client.event = IS_EVENT_ON


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if not isinstance(message.channel, discord.channel.DMChannel):
        return

    if message.content == "!register":
        user = message.author
        event = Register_event(client, user, message)
        await event.register()

    if message.content == "!secrets":
        user = message.author
        await secrets(user)

    if message.author.id in ADMIN_ID:
        if message.content == "!reveal":
            await reveal(client.channel)

        if message.content == "!voters":
            await voters(client, message.author.id)

        if message.content == "!available":
            await available(message.author)

        if message.content == "!start":
            await start_event(client, message.author)


client.run(TOKEN)
