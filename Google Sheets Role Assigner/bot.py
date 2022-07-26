import os
from gsheet_extract import get_info
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

# Update the Nicknames and Roles
@bot.command(name="update")
async def update(ctx, arg):
    # error handling
    if (arg != "comp" and arg != "gen"):
        await ctx.channel.send("BAD ARGUMENT")
        return

    # set the name of the role we need
    if (arg == "comp"):
        role_name = "Comp Team"
    elif (arg == "gen"):
        role_name = "General Member"
    else:
      await ctx.channel.send("BAD ARGUMENT")  
      return
    
    # call the function to extract info
    name_arr, discord_id_arr = get_info(arg)
    for guild in bot.guilds:
        for member in guild.members:
            if (member.name in discord_id_arr):
                # Change Nickname
                name_idx = discord_id_arr.index(member.name)
                # Skip if we have errors (generally going to be privilege errors)
                try:
                    await member.edit(nick=name_arr[name_idx])
                except:
                    continue
                # add role
                role = discord.utils.get(member.guild.roles, name=role_name)
                await member.add_roles(role)
    await ctx.channel.send("Update Completed")

@bot.event
async def on_command_err(ctx,error):
  if isinstance(error, CommandNotFound):
    return
  raise error

keep_alive()
bot.run(TOKEN)
