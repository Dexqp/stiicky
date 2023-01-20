import os
import sys
import json


async def command_setprefix(client, message, config):
    new_prefix = message.content.split()[1]
    if new_prefix:
        config["prefix"] = new_prefix
        with open("config.json", "w") as config_file:
            json.dump(config, config_file, indent=4)
        await message.channel.send(f"Command prefix set to {new_prefix}")
    else:
        await message.channel.send("Please provide a prefix")


async def command_clearall(client, message, config):
    total_deleted = 0
    for channel_id in config["allowed_channels"]:
        channel = client.get_channel(int(channel_id))
        deleted = await channel.purge(check=lambda m: m.author == client.user)
        total_deleted += len(deleted)
    await message.channel.send(f"Deleted {total_deleted} messages across {len(config['allowed_channels'])} channels.")

async def command_clear(client, message, config):
    try:
        amount = int(message.content.split()[1])
    except (ValueError, IndexError):
        return await message.channel.send('Invalid number')
    messages = []
    async for msg in message.channel.history(limit=amount):
        if msg.author == client.user:
            messages.append(msg)
    if messages:
        await message.channel.delete_messages(messages)
        await message.channel.send(f"Deleted previous bot messages.")
    else:
        await message.channel.send("No messages to delete.")


async def command_restart(client, message):
    await message.channel.send("Restarting...")
    os.execl(sys.executable, sys.executable, *sys.argv)

async def command_setmessage(client, message, config):
    channel_id = str(message.channel.id)
    # Extract the message from the command
    new_message = ' '.join(message.content.split()[1:])
    if channel_id not in config['allowed_channels']:
        config['allowed_channels'].append(channel_id)
    config['bot_message'][channel_id] = new_message
    with open('config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)
    await message.channel.send(f'{channel_id} added to allowed channels and message set to: {new_message}')


async def command_rchannel(client, message, config):
    channel_id = str(message.channel.id)
    if channel_id in config['allowed_channels']:
        config['allowed_channels'].remove(channel_id)
        if channel_id in client.counter:
            del client.counter[channel_id]
        with open('config.json', 'w') as config_file:
            json.dump(config, config_file, indent=4)
        await message.channel.send(f'{channel_id} removed from allowed channels')
    else:
        await message.channel.send(f'{channel_id} not in allowed channels')


__all__ = ['command_setprefix', 'command_clearall', 'command_clear', 'command_restart', 'command_setmessage', 'command_rchannel']
