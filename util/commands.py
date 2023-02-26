import os
import sys
import json
import discord
from discord.utils import get




#setprefix
async def command_setprefix(client, message, config):
    """sets the prefix for the bot"""
    new_prefix = message.content.split()[1]
    if new_prefix:
        config["prefix"] = new_prefix
        with open("config.json", "w") as config_file:
            json.dump(config, config_file, indent=4)
        await message.channel.send(f"Command prefix set to {new_prefix}")
    else:
        await message.channel.send("Please provide a prefix")


#setmessage+addchannel
async def command_setmessage(client, message, config):
    channel_id = str(message.channel.id)
    message_content = message.content[len(config["prefix"] + "setmessage "):]
    config["bot_message"][channel_id] = message_content
    if channel_id not in config["allowed_channels"]:
        config["allowed_channels"].append(channel_id)
    if channel_id not in config["thresholds"]:
        config["thresholds"][channel_id] = 1    
    with open("config.json", "w") as config_file:
        json.dump(config, config_file, indent=4)
    await message.channel.send("Successfully set message for this channel.")

#removechannel
async def command_rchannel(client, message, config):
    channel = message.channel
    if str(channel.id) in config["allowed_channels"]:
        config["allowed_channels"].remove(str(channel.id))
        if str(channel.id) in config["thresholds"]:
            del config["thresholds"][str(channel.id)]
        if str(channel.id) in config["bot_message"]:
            del config["bot_message"][str(channel.id)]
        with open("config.json", "w") as config_file:
            json.dump(config, config_file, indent=4)
        await message.channel.send(f"Removed channel {channel.name} from allowed channels.")
    else:
        await message.channel.send(f"Channel {channel.name} is not in allowed channels.")


#treshold
async def command_limit(client, message, config):
    try:
        new_threshold = int(message.content.split()[1])
        config["thresholds"][str(message.channel.id)] = new_threshold
        with open("config.json", "w") as config_file:
            json.dump(config, config_file, indent=4)
        await message.channel.send(f"Threshold for this channel set to {new_threshold}")
    except (ValueError, IndexError):
        await message.channel.send("Please provide a valid threshold")

#help
async def command_help(client, message, config, commands):
    regular_commands = {
        "help": "Shows the list of available commands and their descriptions.",
        "setprefix": "Sets the prefix for server commands.",
        "purge": "Mention a user or amount of messages to delete a maximum of 100 messages per use.",
        "clear": "1-100 - Deletes the specified number of message sent by the bot in the current channel.",
        "setmessage": "Sets the message sent with this command to the current channel and add starts the sticky feature.",
        "rchannel": "Removes the bot's message from the current channel.",
        "restart": "Restarts the bot."
    }
    command_list = "List of available regular commands:\n"
    for command in regular_commands:
        command_list += f"{config['prefix']}{command}\n"
    embed = discord.Embed(title="Commands:", description="A List of available commands", color=0x00FFFF)
    for command in regular_commands:
        embed.add_field(name=command, value=regular_commands.get(command, "No description available"), inline=False)
    await message.channel.send(embed=embed)

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

#purgemessage
async def command_purge(client, message, config):
    # check if there is no user or amount specified in the command
    if len(message.mentions) == 0 and len(message.content.split()) == 1:
        return await message.channel.send("Please mention a user or amount of messages to delete.")

    try:
        amount = int(message.content.split()[-1])
    except (ValueError, IndexError):
        amount = 100

    user = message.mentions[0] if message.mentions else get(client.get_all_members(), id=int(message.content.split()[1]))

    if user is None:
        return await message.channel.send("Please mention a user or specify a valid ID.")

    deleted = await message.channel.purge(limit=amount, check=lambda m: m.author == user)
    await message.channel.send(f"Deleted {len(deleted)} messages.")

#restart
async def command_restart(client, message):
    await message.channel.send("Restarting...")
    os.execl(sys.executable, sys.executable, *sys.argv)

__all__ = ['command_setprefix',
        'command_help',
        'command_clear',
        'command_restart',        
        'command_setmessage',
        'command_rchannel',
        'command_limit',
        'command_purge'
        ]
