from ast import arg
from cmath import exp
from email import message
import gspread
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get
from discord import Embed
# from keep_alive import keep_alive
from discord.ext.commands import CommandNotFound
import pandas as pd
import numpy as np
from table2ascii import table2ascii as t2a, PresetStyle

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(intents=intents, command_prefix='/')

g_todo_table = pd.DataFrame()

@bot.command(name="todo")
async def todo(ctx, *args):
    if (args == None):
        await ctx.channel.send("NO ARGUMENT GIVEN")
        return 

    sa = gspread.service_account(filename="service_account.json")

    # open Google Sheet file by name
    spreadsheet = sa.open("FVE 2022-2023 Logistics")
    sheet = spreadsheet.worksheet("Overview")
    
    # print columns
    if (args[0] == "view" or args[0] == "name"):
        # get rows
        listofdfrows = []
        for i in range(3,100):
            if (len(sheet.row_values(i)) == 0):
                break
            row_list = sheet.row_values(i)
            if (len(row_list) != 5):
                for i in range(5-len(row_list)):
                    row_list.append('')
            listofdfrows.append(row_list)
            

        if (args[0] == "view" and (len(args) == 1 or len(args) == 2)):
            if (len(args) == 2):
                adjusted_table = listofdfrows[:int(args[1])]
            else:
                adjusted_table = listofdfrows
            num_tasks = len(adjusted_table)
            if (num_tasks % 5 == 0):
                num_embeds_needed = num_tasks // 5
            else: 
                num_embeds_needed = num_tasks // 5 + 1

            for i in range(num_embeds_needed):
                embed = Embed(title="To-do Table (" + str(i+1) + " of " + str(num_embeds_needed) + ")")
                for j in range(5):
                    if (i*5+j >= num_tasks):
                        break
                    embed.add_field(
                        name=f'**{adjusted_table[i*5+j][0]}**', 
                        value=f'> People Responsible: {adjusted_table[i*5+j][1]}\n> Expected Due Date: {adjusted_table[i*5+j][2]}\n> Completion Date: {adjusted_table[i*5+j][3]}\n> Notes: {adjusted_table[i*5+j][4]}',
                        inline=False
                    )
                await ctx.channel.send(embed=embed)
        
        elif (args[0] == "name" and len(args) == 2):
            embed = Embed(title="Tasks for " + args[1])
            for row in listofdfrows:
                if (args[1] in row[1]):
                    embed.add_field(
                        name=f'**{row[0]}**', 
                        value=f'> People Responsible: {row[1]}\n> Expected Due Date: {row[2]}\n> Completion Date: {row[3]}\n> Notes: {row[4]}',
                        inline=False
                    )
            if (len(embed.fields) == 0):
                embed.add_field (
                    name=f'**No Tasks**',
                    value = f'No Tasks Available for {args[1]}'
                )
            await ctx.channel.send(embed=embed)

    # update the completion date
    # args[1] -> task name
    # args[2] -> date
    elif(args[0] == "complete"):
        if (len(args) != 3):
            await ctx.channel.send("INVALID ARGUMENTS")
            return
        
        # get rows
        listofdfrows = []
        for i in range(3,100):
            if (len(sheet.row_values(i)) == 0):
                break
            row_list = sheet.row_values(i)
            if (len(row_list) != 5):
                for i in range(5-len(row_list)):
                    row_list.append('')
            listofdfrows.append(row_list)

        for i in range(len(listofdfrows)):
            if (args[1] in listofdfrows[i][0]):
                sheet.update_cell(i+3, 4, args[2])
                break

    # create new to-do: need name of Task, People Responsible, Due Date, Notes
    elif(args[0] == "add"):
        if (len(args) != 5 and len(args) != 4):
            await ctx.channel.send("INVALID ARGUMENTS")
            return
        
        # find next empty row
        i = 1
        for i in range(1,100):
            if (len(sheet.row_values(i)) == 0):
                break
        row = i

        # found empty row, now add to sheet
        sheet.update_cell(row, 1, args[1])
        sheet.update_cell(row, 2, args[2])
        sheet.update_cell(row, 3, args[3])
        if (len(args) == 4):
            sheet.update_cell(row, 5, '')
        else:
            sheet.update_cell(row, 5, args[4])

            
    # delete row when to-do is not needed
    elif(args[0] == "delete"):
        if (len(args) != 2):
            await ctx.channel.send("INVALID ARGUMENTS")
            return

        # get rows
        listofdfrows = []
        for i in range(3,100):
            if (len(sheet.row_values(i)) == 0):
                break
            row_list = sheet.row_values(i)
            if (len(row_list) != 5):
                for i in range(5-len(row_list)):
                    row_list.append('')
            listofdfrows.append(row_list)
        for i in range(len(listofdfrows)):
            if (args[1] in listofdfrows[i][0]):
                sheet.delete_rows(i+3)
                break

        await ctx.channel.send("Command Not Finished")
    
    else: 
        await ctx.channel.send("BAD ARGUMENTS")




@bot.event
async def on_command_err(ctx,error):
  if isinstance(error, CommandNotFound):
    return
  raise error

# keep_alive()
bot.run(TOKEN)