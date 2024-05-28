import discord
import asyncio

from config import TOKEN
from timer import Timer

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.dm_messages = True
intents.dm_reactions = True
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

    def check_if_private(secret):
        return secret.author == message.author and isinstance(
            secret.channel, discord.channel.DMChannel
        )

    def check_reaction_emoji(reaction, user):
        return str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌"

    if message.content.startswith("!register"):
        user = message.author
        await user.send("Parfait, j'écoute ton secret !")
        secret = await client.wait_for("message", check=check_if_private)

        msg = await user.send(
            f"D'accord, ton secret est-il bien : \n\n {secret.content}"
        )
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")

        try:
            reaction, user = await client.wait_for(
                "reaction_add", timeout=30, check=check_reaction_emoji
            )

        except asyncio.TimeoutError:
            await user.send(
                "Tu as mis trop longtemps à répondre, ton secret n'a pas été enregistré."
            )

        else:
            match str(reaction):
                case "✅":
                    await user.send("Ton secret a bien été enregistré")

                case "❌":
                    await user.send("Ton secret n'a pas été enregistré")


client.run(TOKEN)
