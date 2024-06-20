import time
import datetime

from config import cursor, conn, IS_EVENT_ON


def register_secret(secret, user_id):
    """Enregistre un secret dans la base de données"""

    # Check si l'utilisateur existe dans la base de données
    cursor.execute("SELECT * from users WHERE user_id LIKE %s;", [user_id])
    user = cursor.fetchone()

    # Si non: l'ajoute
    if not user:
        user = cursor.execute(
            "INSERT INTO users (user_id, number_secrets) VALUES (%s, %s)",
            (user_id, 0),
        )

    # Enregistre le secret dans la base de données
    cursor.execute(
        "INSERT INTO secrets (secret, user_id, available) VALUES (%s, %s, %s)",
        (secret, user[0], True),
    )
    # Update le nombre de secret de l'utilisateur
    cursor.execute(
        "UPDATE users SET number_secrets=%s WHERE id=%s;", (user[2] + 1, user[0])
    )
    conn.commit()

    message = f"Votre secret a bien été enregistré ! Vous avez {user[2] + 1} secrets"

    return message


async def get_secret(channel):
    """Tire un secret au hasard dans la base de données"""

    number_of_available_secrets = count_available_secrets()

    # Pour participer, un utilisateur doit avoir enregistré au moins 2 secrets.
    cursor.execute(
        "SELECT * FROM secrets JOIN users ON secrets.user_id = users.id WHERE available IS TRUE AND number_secrets > 1 ORDER BY RANDOM() LIMIT 1;"
    )
    secret = cursor.fetchone()

    # Update le secret pour qu'il ne soit plus tiré
    cursor.execute("UPDATE secrets SET available=%s WHERE id=%s;", [False, secret[0]])
    conn.commit()

    if number_of_available_secrets == 1:
        await channel.send(
            "C'est le dernier secret, l'évènement va se terminer, merci à tous d'avoir participé 🙂 !"
        )
    date = datetime.datetime.now().strftime("%d/%m/%Y")
    return f"""Secret du jour {date}:\n" **{secret[1]}** "\nÀ qui appartient ce secret ? Vous avez jusqu'à 14h pour faire une proposition. Bonne chance !"""


def count_available_secrets():
    cursor.execute(
        "SELECT COUNT(*) FROM secrets JOIN users ON secrets.user_id = users.id WHERE available IS TRUE AND number_secrets > 1;"
    )
    return cursor.fetchone()[0]


def get_participants():
    cursor.execute("SELECT * FROM users WHERE number_secrets > 1;")
    return cursor.fetchall()


def get_secret_numbers(user):
    cursor.execute(
        "SELECT * FROM secrets JOIN users ON secrets.user_id = users.id WHERE users.user_id LIKE %s;",
        [str(user.id)],
    )
    return cursor.fetchall()


def is_participating(client, user_id):
    print("rentre dans is_participating")
    print(f"event : {client.event}")

    if client.event == True:
        try:
            print(f"num secrets : {get_secret_numbers(user_id)}")
            print(f"len : {len(get_secret_numbers(user_id))}")
            if len(get_secret_numbers(user_id)) > 1:
                return True
            return False
        except:
            print("passe dans False")
            return False
