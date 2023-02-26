import discord
from collections import defaultdict



async def sticker(client, message, config, semaphore, previous_message, counter):
    client.counter = defaultdict(int, client.counter)
    if message.author != client.user and (not config["allowed_channels"] or str(message.channel.id) in config["allowed_channels"]):
        async with semaphore:
            client.counter[str(message.channel.id)] += 1
            if client.counter[str(message.channel.id)] == config["thresholds"][str(message.channel.id)]:
                bot_message = config["bot_message"].get(str(message.channel.id), "default message")
                prev_msg = client.previous_message.get(str(message.channel.id))
                if prev_msg:
                    try:
                        await prev_msg.delete()
                    except discord.errors.NotFound:
                        pass
                client.previous_message[str(message.channel.id)] = await message.channel.send(bot_message)
                client.counter[str(message.channel.id)] = 0