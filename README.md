# stiicky
A discord bot that allows you to keep sticky messages at the bottom of a channel.
Instructions:
1.    Open sticky.py or stickybot.exe if you downloaded the exe
2.    The bot will close itself and create a JSON file, open the JSON file with a text editor
3.    Enter your bot token and then enter the channel IDs of the channels you want the bot to run in under "bot_message" and "allowed       channels" (replace the channel_id_1in both instances but keep the "").
4.    Replace the "message 1\nThis will be in a new line" per channel (this can be different per channel),n "\n" will create a new line, if you don't put it in, everything will be in a single line.
5.    Reastart the bot and you will see "Bot is ready" on the console.


# commands
!clearall - Deletes all previously sent messages by the bot in all channels in the server
!clear [1-100] - Clears specified no.of messages sent by the bot in the channel.
!restart - Restarts the bot (use this if you made changes to the json while it's running
!setmessage [message here] - Adds the channel you type this in into "Allowed channels" and sets the message to be stickied in that channel
!rchannel - Removes the channel from allowed channels.
!setprefix - sets what command you want to set. This is "!" by default.
