import json
import os
import asyncio
import discord
from util.sticky import sticker
from util.commands import *


intents = discord.Intents.all()
client = discord.Client(intents=intents)

# check if config.json exists, if not, create it with default values
if os.path.isfile("config.json"):
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    default_config = {
        "token": "YOUR_BOT_TOKEN",
        "bot_message": {
            "channel_id_1": "message 1\nThis will be in a new line"
        },
        "allowed_channels": ["channel_id_1"],
        "thresholds": {},
        "prefix": "!"
    }
    keys_to_check = ["thresholds", "prefix"]
    for key in keys_to_check:
        if key not in config:
            config[key] = default_config[key]
    with open("config.json", "w") as config_file:
        json.dump(config, config_file, indent=4)
else:
    with open("config.json", "w") as config_file:
        default_config = {
            "token": "YOUR_BOT_TOKEN",
            "bot_message": {
                "channel_id_1": "message 1\nThis will be in a new line"
            },
            "allowed_channels": ["channel_id_1"],
            "thresholds": {},
            "prefix": "!"
        }
        json.dump(default_config, config_file, indent=4)

# load the configuration from a json file
with open("config.json") as config_file:
    config = json.load(config_file)

#number of messages the bot can send at a time (keep this at 1)
semaphore = asyncio.Semaphore(1)
client.counter = {channel: 0 for channel in config["allowed_channels"]}
client.previous_message = {}

commands = {name[8:]: function for name, function in globals().copy().items() if name.startswith("command_")}


@client.event
async def on_message(message):
    if message.content.startswith(config["prefix"]):
        command = message.content[len(config["prefix"]):].split()[0]
        if command in commands:
            if message.author.guild_permissions.manage_channels:
                if command == "help":
                    await commands[command](client, message, config, commands)
                    await message.delete()
                elif command == "restart":
                    await commands[command](client, message)
                    await message.delete()
                else:
                    await commands[command](client, message, config)
                    await message.delete()
            else:
                await message.channel.send("You do not have the permission to run this command.")
                await message.delete()
    else:
        await sticker(client, message, config, semaphore, client.previous_message, client.counter)




@client.event
async def on_ready():
    print("Bot is ready!")

client.counter = {channel: 0 for channel in config["allowed_channels"]}
client.previous_message = {}
client.run(config["token"])