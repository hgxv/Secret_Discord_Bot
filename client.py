import discord
import asyncio

from config import TOKEN
from timer import Timer

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.dm_messages = True
intents.dm_reactions = True

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

    def check_if_private(secret):
        return secret.author == message.author and isinstance(
            secret.channel, discord.channel.DMChannel
        )

    def check_reaction_emoji(reaction, user):
        print(reaction)
        print(str(reaction.emoji))
        return str(reaction.emoji) == "✅"

    if message.content.startswith("!register"):
        user = message.author
        await user.send("Parfait, j'écoute ton secret !")
        secret = await client.wait_for("message", check=check_if_private)

        msg = await user.send(
            f"D'accord, ton secret est-il bien : \n\n {secret.content}"
        )
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")


client.run(TOKEN)
