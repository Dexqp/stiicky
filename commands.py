import os
import sys

async def command_clearall(client, message, config):
    total_deleted = 0
    for channel_id in config["allowed_channels"]:
        channel = client.get_channel(int(channel_id))
        deleted = await channel.purge(check=lambda m: m.author == client.user)
        total_deleted += len(deleted)
    await message.channel.send(f"Deleted {total_deleted} messages across {len(config['allowed_channels'])} channels.")

async def command_restart(client, message):
    await message.channel.send("Restarting...")
    os.execl(sys.executable, sys.executable, *sys.argv)


__all__ = ['command_clearall', 'command_restart']
