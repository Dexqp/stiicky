import json
import os
import asyncio
import discord
from commands import *


intents = discord.Intents.all()
client = discord.Client(intents=intents)

# check if config.json exists, if not, create it with default values
if not os.path.isfile("config.json"):
    with open("config.json", "w") as config_file:
        default_config = {
            "token": "YOUR_BOT_TOKEN",
            "bot_message": {
                "channel_id_1": "message 1\nThis will be in a new line",
                "channel_id_2": "message 1\nThis will be in a new line",
                "channel_id_3": "message 1\nThis will be in a new line"
            },
            "allowed_channels": ["channel_id_1", "channel_id_2", "channel_id_3"],
            "threshold": 1,
            "allowed_role": "admin"
        }
        json.dump(default_config, config_file, indent=4)

# load the configuration from a json file
with open("config.json") as config_file:
    config = json.load(config_file)

#number of messages the bot can send at a time (keep this at 1)
semaphore = asyncio.Semaphore(1)

commands = {}
for name, function in globals().copy().items():
    if name.startswith("command_"):
        commands[name[8:]] = function

@client.event
async def on_message(message):
    if message.author != client.user and (not config["allowed_channels"] or str(message.channel.id) in config["allowed_channels"]):
        async with semaphore:
            client.counter[str(message.channel.id)] += 1
            if client.counter[str(message.channel.id)] == config["threshold"]:
                bot_message = config["bot_message"].get(str(message.channel.id), "default message")
                prev_msg = client.previous_message.get(str(message.channel.id))
                if prev_msg:
                    try:
                        await prev_msg.delete()
                    except discord.errors.NotFound:
                        pass
                client.previous_message[str(message.channel.id)] = await message.channel.send(bot_message)
                client.counter[str(message.channel.id)] = 0
    if message.content.startswith("!"):
        command = message.content[1:].split()[0]
        if command in commands:
            allowed_role = discord.utils.get(message.guild.roles, name=config['allowed_role'])
            if allowed_role in message.author.roles:
                if command == 'restart':
                    await commands[command](client, message)
                else:
                    await commands[command](client, message, config)
            else:
                await message.channel.send("You do not have the permission to run this command.")


@client.event
async def on_ready():
    print("Bot is ready!")

client.counter = {channel: 0 for channel in config["allowed_channels"]}
client.previous_message = {}
client.run(config["token"])
