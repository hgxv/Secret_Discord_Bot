import discord

from config import TOKEN
from database import register_secret

intents = discord.Intents.default()
intents.message_content = True

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

    else:

        def check(secret):
            return secret.author == message.author and isinstance(
                secret.channel, discord.channel.DMChannel
            )

        if message.content.startswith("!register"):
            await message.author.send("Parfait, j'écoute ton secret !")
            secret = await client.wait_for("message", check=check)

            try:
                register_secret(secret.content, secret.author.id)

            except:
                await message.author.send(
                    "J'ai eu un petit soucis, merci d'informer les patrons !"
                )
                return

            await message.author.send(
                f"D'accord, ton secret est bien : \n\n {secret.content}"
            )


client.run(TOKEN)
