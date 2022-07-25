import os
from gsheet_writeto import write_data_to_sheet
import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord.utils import get
from datetime import datetime
from discord import Embed
from discord.ext.commands import Cog
from keep_alive import keep_alive
from discord.ext.commands import CommandNotFound


# setup 
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
SERVER_ID = os.getenv('SERVER_ID')

intents = discord.Intents.default()
intents.members = True

# yes/no symbols
emojis = ['✅', '❌']
options = ['Yes', 'No']

bot = commands.Bot(intents=intents, command_prefix='/')

'''
Poll Creation
'''
@bot.command(name="attendpoll")
async def attendpoll(ctx, channel: discord.TextChannel, date: str):
    
    embed = Embed(title = "Are you coming to practice on " + date + "?",
                description = "Attendance Poll",
                timestamp = datetime.utcnow())
    
    fields = [("Options", "\n".join([f"{emojis[idx]} {option}" for idx, option in enumerate(options)]), False),
					  ("Instructions", "React to cast a vote!", False)]

    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline) 

    message = await channel.send(embed=embed)
    poll_message_id = message.id

    for emoji in emojis:
        await message.add_reaction(emoji)
    
    await channel.send("Poll ID: " + str(poll_message_id))


'''
Function used to end poll and transfer results into spreadsheet
'''
@bot.command(name="endattendpoll")
async def endattendpoll(ctx, channel: discord.TextChannel, message_id: int):
    # grab responses
    message = await channel.fetch_message(message_id)
    yes_users = []
    no_users = []
    for reaction in message.reactions:
        async for user in reaction.users():
            if (user.id == 998478965834535024):
                continue
            if (str(reaction) == emojis[0]):
                yes_users.append(user.nick)
            elif (str(reaction) == emojis[1]):
                no_users.append(user.nick)

    # get Date
    date_str = ''
    for embed in message.embeds:
        title_split = embed.title.split(" ") 
        date_str = title_split[6].split("?")[0]

    # write to spreadsheet
    write_data_to_sheet(yes_users, no_users, date_str)
    
    # delete poll
    await message.delete()

    await ctx.channel.send("Spreadsheet is updated - https://docs.google.com/spreadsheets/d/1r8-_bWm8hsmeGGhhja0vH86IvmbR982U3fzF-ko7CHo/edit#gid=1646081339")


'''
Display a message when a user adds reaction to a poll
'''
@bot.event
async def on_raw_reaction_add(ctx):
    # grab channel info to print in
    channel_id = ctx.channel_id
    if (channel_id != 995125304152571924 and channel_id != 995591357617938442): #comp-attendance, #bot-spam
        return
    channel = bot.get_channel(channel_id)
    
    # grab user that reacted
    user_id = ctx.user_id
    if (user_id == 998478965834535024): # ignore if bot reaction
        return
    user = bot.get_user(user_id)

    # get user's nickname
    nickname_user = ''
    for guild in bot.guilds:
        for member in guild.members:
            if (member == user):
                nickname_user = member.nick

    #grab message that was reacted on
    message_id = ctx.message_id
    message = await channel.fetch_message(message_id)

    # get Date
    date_str = ''
    for embed in message.embeds:
        title_split = embed.title.split(" ") 
        date_str = title_split[6].split("?")[0]

    result_str = ""
    if (str(ctx.emoji) == emojis[0]):
        result_str = "yes"
    elif (str(ctx.emoji) == emojis[1]):
        result_str = "no"
    else:
        result_str = "Follow directions SMH"
    
    # print that someone reacted
    await channel.send(f"{nickname_user} responded {result_str} to practice on {date_str}")

'''
Display a message when a user removes reaction to a poll
'''
@bot.event
async def on_raw_reaction_remove(ctx):
    # grab channel info to print in
    channel_id = ctx.channel_id
    if (channel_id != 995125304152571924 and channel_id != 995591357617938442): #comp-attendance, #bot-spam
        return
    channel = bot.get_channel(channel_id)
    
    # grab user that reacted
    user_id = ctx.user_id
    if (user_id == 998478965834535024): # ignore if bot reaction
        return
    user = bot.get_user(user_id)

    # get user's nickname
    nickname_user = ''
    for guild in bot.guilds:
        for member in guild.members:
            if (member == user):
                nickname_user = member.nick

    #grab message that was reacted on
    message_id = ctx.message_id
    message = await channel.fetch_message(message_id)

    # get Date
    for embed in message.embeds:
        title_split = embed.title.split(" ") 
        date_str = title_split[6].split("?")[0]
    
    # print that someone reacted
    await channel.send(f"{nickname_user} removed their vote for practice on {date_str}")       

@bot.event
async def on_command_err(ctx,error):
  if isinstance(error, CommandNotFound):
    return
  raise error

keep_alive()
bot.run(TOKEN)