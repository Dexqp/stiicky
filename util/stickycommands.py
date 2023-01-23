import json
import discord




#helpstickybot
async def command_helpsticky(client, message, config, commands):
    sticky_commands = {
        "setmessage": "Sets the message sent with this command to the current channel and add starts the sticky feature.",
        "rchannel": "Removes the bot's message from the current channel."
    }
    command_list = "List of available sticky commands:\n"
    for command in sticky_commands:
        command_list += f"{config['prefix']}{command}\n"
    embed = discord.Embed(title="Sticky Commands:", description="A List of available commands", color=0x00FFFF)
    for command in sticky_commands:
        embed.add_field(name=command, value=sticky_commands.get(command, "No description available"), inline=False)
    await message.channel.send(embed=embed)



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

#treshold
async def command_limit(client, message, config):
    try:
        new_threshold = int(message.content.split()[1])
        config["threshold"] = new_threshold
        with open("config.json", "r+") as config_file:
            config_file.write(json.dumps(config, indent=4))
        await message.channel.send(f"Threshold set to {new_threshold}")
    except (ValueError, IndexError):
        await message.channel.send("Please provide a valid threshold")



__all__ = ['command_helpsticky',
        'command_setmessage',
        'command_rchannel',
        'command_limit'
        ]