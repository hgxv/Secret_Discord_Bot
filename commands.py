import discord
import asyncio

from database import register_secret, get_secret


async def register(message, user, client):

    # Check si le message est un message privé
    def check_if_private(secret):
        return secret.author == message.author and isinstance(
            secret.channel, discord.channel.DMChannel
        )

    # Check si l'utilisateur réagit au message
    def check_reaction_emoji(reaction, user):
        return str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌"

    await user.send("Parfait, j'écoute ton secret !")
    secret = await client.wait_for("message", check=check_if_private)

    msg = await user.send(f"D'accord, ton secret est-il bien : \n\n {secret.content}")
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
                await user.send(register_secret(secret.content, str(user.id)))

            case "❌":
                await user.send("Ton secret n'a pas été enregistré")


async def reveal(channel):
    secret = await get_secret(channel)
    await channel.send(secret)
