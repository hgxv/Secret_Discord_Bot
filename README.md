# What is this ?

This project is a discord bot which allow you to play a game of secrets. 

People will tell the bot some secrets that will be stocked in the database.
The game is that each day, a random secret will be chosen at random, and people will have to guess whose secret it is.


# Preparation

This project needs python and postgresql to work.
Command lines in this doc are indicated for a Unix use.

## Create the database

First, access the postgres commandline to create an account:

`sudo -u postgres psql`

You should now be in the postgres commandline :

![image](https://github.com/hgxv/Secret_Discord_Bot/assets/13985587/a34efe92-65e0-41ab-8675-7837152cbf88)

You can now create a new superuser :

` CREATE ROLE username WITH LOGIN SUPERUSER PASSWORD 'password'; `

While you're here, create your future database:

` CREATE DATABASE secrets `

No need to create any tables, the script will do it for you.
(the database's name is actually hardcoded as "secrets", you can change it in config.py on line 16)


## Create your environment

First, make sure you are in the correct folder.

` python3 -m venv env `

Activate the environment you just created.

` source env/Scripts/activate `

You should have (env) before your session on the command line now, indicated it is activated:
![image](https://github.com/hgxv/Secret_Discord_Bot/assets/13985587/07e1f5d5-9f70-46e2-8de0-1b214773aeb6)

Then, you can install dependencies with :

` python3 -m pip install -r requirements.txt `

Create a .env file at the root of the project containing following parameters:

```
TOKEN="your_discord_app_token"
DB_PORT="5432"
DB_USER="Your_username"
DB_PASS="Your_password"
ADMIN_ID=" * "
CHANNEL=" ** "
```

\* : ADMIN_ID will determine which persons will have access to admin commands of the bot, be careful. To get the user's discord ID, right click on them and select the last option

![image](https://github.com/hgxv/Secret_Discord_Bot/assets/13985587/23a17e4a-4aaa-48af-b02b-6d4801542a79)

In case you want multiple persons to have access, you can, just seperate ids with commas.
Example :
` ADMIN_ID = "2222222222222, 1111111111, 3333333333333" `

\** : CHANNEL will determine where the bot will reveal secrets. Following ADMIN_ID's example, right click on the channel and copy it's ID. Only one channel can be selected, be careful.

The bot should now be ready, just enter the following command to launch it:

` python3 client.py `

# How does it work ?

To participate, users must have at least 2 secrets registered before the event start. After that, only people with at least 2 secrets can keep registering secrets.
Everything is happening with written commands with the "!" prefix. Nothing will be written in public, every command must be typed in private to the bot.

**It has been decided for this project that the counting and scoring will be done manually**

Here is the list of public commands :

* `!register` : The bot will ask you what your secret is. Then you have some time to check your secret is well written and validate *
* `!secrets` : The bot will tell you how many secrets you have.
* 
\* Example :

![image](https://github.com/hgxv/Secret_Discord_Bot/assets/13985587/f0337b83-356a-42e1-9cea-bb4cdb05f9da)

___

Here are the admin commands :

* `!reveal` : The bot will chose at random a new secret and display it to the game channel
* `!voters` : The bot will tell you who is a valid participant (at least 2 secrets)
* `!available` : The bot will tell you how many secrets are left in the database
* `!start` : The event will start, and people that doesn't have their 2 secrets registered won't be able to participate anymore

Well now, enjoy !

If you find any bug/mistake, bring it up !
