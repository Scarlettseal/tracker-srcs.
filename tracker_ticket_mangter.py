import discord
from discord.ext import commands

# Create bot instance with command prefix
intents = discord.Intents.default()
intents.members = True  # Make sure the bot has permission to read messages and member data
bot = commands.Bot(command_prefix="!", intents=intents)

# Define the role ID you want to ping
ROLE_ID = 1302831243116806224  # Replace with the actual role ID

@bot.event
async def on_guild_channel_create(channel):
    # Check if the channel name contains "ticket"
    if "ticket" in channel.name.lower():
        # Get the role object using the role ID
        role = discord.utils.get(channel.guild.roles, id=ROLE_ID)
        if role:
            # Send a message to the new channel, pinging the role
            await channel.send(f"{role.mention} hello welcome, how would you like to pay?")

# Run the bot with your token
bot.run('MTMwNDk3NjQ0OTYxNDI1MDA5NQ.Gp2M31.UdaQUYE1edT0njfi3A86ydeuOt5XS5z5kacbNA')
