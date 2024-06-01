import time

from config import cursor, conn


def register_secret(secret, user_id):
    print(f"{secret}, {user_id}")
    print(type(user_id))

    cursor.execute("SELECT * from users WHERE user_id LIKE %s;", [user_id])
    user = cursor.fetchone()

    if not user:
        user = cursor.execute(
            "INSERT INTO users (user_id, number_secrets) VALUES (%s, %s)",
            (user_id, 0),
        )

    cursor.execute(
        "INSERT INTO secrets (secret, user_id, available) VALUES (%s, %s, %s)",
        (secret, user[0], True),
    )
    cursor.execute(
        "UPDATE users SET number_secrets=%s WHERE id=%s;", (user[2] + 1, user[0])
    )
    conn.commit()

    message = f"Votre secret a bien été enregistré ! Vous avez {user[2] + 1} secrets"

    return message


async def get_secret(channel):
    cursor.execute(
        "SELECT * FROM secrets WHERE available IS TRUE ORDER BY RANDOM() LIMIT 1;"
    )
    secret = cursor.fetchone()
    cursor.execute("UPDATE secrets SET available=%s WHERE id=%s;", (False, secret[0]))

    cursor.execute(
        "SELECT COUNT(*) FROM secrets WHERE available IS TRUE ORDER BY RANDOM() LIMIT 1;"
    )
    number_of_available_secrets = cursor.fetchone()[0]

    if number_of_available_secrets == 0:
        await channel.send(
            "C'est le dernier secret, l'évènement va se terminer, merci à tous d'avoir participé :) !"
        )
        time.sleep(2)

    conn.commit()

    return f"Voici le secret d'aujourd'hui :\n\n **{secret[1]}**"
