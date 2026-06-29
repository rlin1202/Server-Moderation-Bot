# Server-Moderation-Bot
 Discord bot for server moderation, member tracking, emote management,<br>
 later features including music playback, sports boxscores, and anything other niches that users would be interested in.<br>

 #Features 
 Moderation commands: kick, ban (permanent, timeout, warn, clear, mute (reconsidering because of built in timeout function)
 Welcome/Goodbye message embeds
 Emote management and importing emotes from other servers, links, and files 
 Infraction history
 Automodding (WIP)

#Requirements
Python 3.10+
PostgreSQL database
Discord bot token with the following intents enabled:
  GUILD_MEMBERS (for on_member_join/remove)
  MESSAGE_CONTENT (for prefix commands)

#Setup

run pip install -r requirements.txt<br>
make .env in the source directory and put api keys

#Bot Permissions Required
Kick Members
Ban Members
Moderate Members (for timeout)
Manage Messages (for clear)
Manage Emojis
Manage Channels

#Documentation used and referenced:<br>
https://docs.discord.com/developers/quick-start/getting-started<br>
https://docs.discord.com/developers/resources/user<br>
https://discordpy.readthedocs.io/en/stable/api.html<br>
