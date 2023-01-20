import os
import sys
import json



#setprefix
async def command_setprefix(client, message, config):
    """
    Usage: !ping
    Description: Pings the bot and returns 'Pong!'
    """
    new_prefix = message.content.split()[1]
    if new_prefix:
        config["prefix"] = new_prefix
        with open("config.json", "w") as config_file:
            json.dump(config, config_file, indent=4)
        await message.channel.send(f"Command prefix set to {new_prefix}")
    else:
        await message.channel.send("Please provide a prefix")


#help
async def command_hjhj(client, message, config, commands):
    """
    Sends a message listing all available commands and their descriptions.
    """
    help_text = "List of available commands:\n"
    for command, function in commands.items():
        if command.startswith("command_"):
            help_text += f"{command[8:]}: {function.__doc__}\n"
    await message.channel.send(help_text)


#clearallmessage
async def command_clearall(client, message, config):
    total_deleted = 0
    for channel_id in config["allowed_channels"]:
        channel = client.get_channel(int(channel_id))
        deleted = await channel.purge(check=lambda m: m.author == client.user)
        total_deleted += len(deleted)
    await message.channel.send(f"Deleted {total_deleted} messages across {len(config['allowed_channels'])} channels.")

#clearmessage
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

#restart
async def command_restart(client, message):
    await message.channel.send("Restarting...")
    os.execl(sys.executable, sys.executable, *sys.argv)

#setmessage+addchannel
async def command_setmessage(client, message, config):
    channel_id = str(message.channel.id)
    message_content = message.content[len(config["prefix"] + "setmessage "):]
    config["bot_message"][channel_id] = message_content
    if channel_id not in config["allowed_channels"]:
        config["allowed_channels"].append(channel_id)
    with open("config.json", "w") as config_file:
        json.dump(config, config_file, indent=4)
    await message.channel.send("Successfully set message for this channel.")

#removechannel
async def command_rchannel(client, message, config):
    channel = message.channel
    if str(channel.id) in config["allowed_channels"]:
        config["allowed_channels"].remove(str(channel.id))
        del config["bot_message"][str(channel.id)]
        with open("config.json", "w") as config_file:
            json.dump(config, config_file, indent=4)
        await message.channel.send(f"Removed channel {channel.name} from allowed channels.")
    else:
        await message.channel.send(f"Channel {channel.name} is not in allowed channels.")


__all__ = ['command_setprefix', 'command_clearall', 'command_clear', 'command_restart', 'command_setmessage', 'command_rchannel']
