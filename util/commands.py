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


#help
async def command_helpbot(client, message, config, commands):
    regular_commands = {
        "help": "Shows the list of available commands and their descriptions.",
        "setprefix": "Sets the prefix for server commands.",
        "purge": "Tries to delete all messages sent by the bot in the server.",
        "clear": "1-100 - Deletes the specified number of message sent by the bot in the current channel.",
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

#restart
async def command_restart(client, message):
    await message.channel.send("Restarting...")
    os.execl(sys.executable, sys.executable, *sys.argv)



__all__ = ['command_setprefix',
        'command_helpbot',
        'command_clear',
        'command_restart'
        ]
