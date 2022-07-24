import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get
from keep_alive import keep_alive
from discord.ext.commands import CommandNotFound

# setup 
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(intents=intents, command_prefix='/')

@bot.command()
async def clean(ctx):
    for guild in bot.guilds:
        for member in guild.members:
            if (member.nick == None and member.bot == False):
                try:
                    reason = "No Nickname Provided"
                    await ctx.guild.kick(member)
                    await ctx.send(f'User {member.mention} has been kicked for {reason}')
                except:
                    continue
    await ctx.channel.send("Clean Members Completed")

@bot.event
async def on_command_err(ctx,error):
  if isinstance(error, CommandNotFound):
    return
  raise error

keep_alive()
bot.run(TOKEN)