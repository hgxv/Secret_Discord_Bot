import discord
import asyncio

from config import TOKEN, CHANNEL, ADMIN_ID
from commands import register, reveal

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if not isinstance(message.channel, discord.channel.DMChannel):
        return

    if message.content == "!register":
        user = message.author
        await register(message, user, client)

    if message.author.id in ADMIN_ID:
        channel = client.get_channel(CHANNEL)
        if message.content == "!reveal":
            reveal(channel)


client.run(TOKEN)
