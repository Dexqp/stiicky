import os
import sys
import json
import discord
from discord.utils import get






#help
async def command_help(client, message, config, commands):
    regular_commands = {
        "help": "Shows the list of available commands and their descriptions.",
        "helpbot": "Shows the list of bot commands and their descriptions", 
        "helpsticky": "Shows the list of Stickybot commands and their descriptions",       
        "purge": "Mention a user or amount of messages to delete a maximum of 100 messages per use."
        
    }
    command_list = "List of available commands:\n"
    for command in regular_commands:
        command_list += f"{config['prefix']}{command}\n"
    embed = discord.Embed(title="Commands:", description="A List of available commands", color=0x00FFFF)
    for command in regular_commands:
        embed.add_field(name=command, value=regular_commands.get(command, "No description available"), inline=False)
    await message.channel.send(embed=embed)





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



__all__ = ['command_help',
        'command_purge'
        ]