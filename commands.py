import discord
import asyncio

from config import IS_EVENT_ON

from database import (
    register_secret,
    get_secret,
    get_participants,
    get_secret_numbers,
    count_available_secrets,
    is_participating,
    set_event_on,
)


class Register_event:
    def __init__(self, client, user, message):
        self.client = client
        self.user = user
        self.message = message
        self.channel = client.channel

    async def register(cls):
        # Check si le message est un message privé
        def check_if_private(secret):
            return secret.author == cls.message.author and isinstance(
                secret.channel, discord.channel.DMChannel
            )

        # Check si l'utilisateur réagit au message
        def check_reaction_emoji(reaction, user):
            return user == cls.user and (
                str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌"
            )

        # Si l'event a déjà commencé, vérifie que l'user participe bien.
        if (
            cls.client.event == True
            and is_participating(cls.client, cls.user.id) is False
        ):
            await cls.user.send(
                "L'évènement a déjà commencé, vous ne pouvez plus participer."
            )
            return

        await cls.user.send("Parfait, j'écoute ton secret !")
        secret = await cls.client.wait_for("message", check=check_if_private)

        msg = await cls.user.send(
            f"D'accord, ton secret est-il bien : \n\n {secret.content}"
        )
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")

        try:
            reaction, user = await cls.client.wait_for(
                "reaction_add", timeout=60, check=check_reaction_emoji
            )

        except asyncio.TimeoutError:
            await cls.user.send(
                "Tu as mis trop longtemps à répondre, ton secret n'a pas été enregistré."
            )

        else:
            match str(reaction):
                case "✅":
                    await cls.user.send(
                        register_secret(secret.content, str(cls.user.id))
                    )

                case "❌":
                    await cls.user.send("Ton secret n'a pas été enregistré")


async def reveal(channel):
    secret = await get_secret(channel)
    await channel.send(secret)


async def voters(client, user):
    user = client.get_user(user)
    voters_list = "\n- ".join(
        [client.get_user(int(user[1])).mention for user in get_participants()]
    )
    message = "Voici la liste des participants :\n- "
    await user.send(message + voters_list)


async def secrets(user):
    tab = get_secret_numbers(user)
    revealed_number = len([revealed for revealed in tab if revealed[2] is False])
    await user.send(
        f"Vous avez {len(tab)} secrets dont {revealed_number} ont déjà été révélés"
    )


async def available(user):
    await user.send(
        f"Il reste {count_available_secrets()} secrets disponibles dans la banque"
    )


async def start_event(client, user):
    client.event = True
    set_event_on()
    await user.send("L'event a bien démarré")
