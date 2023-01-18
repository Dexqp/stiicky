import json
import os
import asyncio
import discord

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
            "threshold": 1
        }
        json.dump(default_config, config_file, indent=4)

# load the configuration from a json file
with open("config.json") as config_file:
    config = json.load(config_file)

semaphore = asyncio.Semaphore(1)

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

@client.event
async def on_ready():
    print("Bot is ready!")

client.counter = {channel: 0 for channel in config["allowed_channels"]}
client.previous_message = {}
client.run(config["token"])
