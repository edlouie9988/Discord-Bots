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

    # get first 4 columns and put into a text table
    
    # print columns
    if (args[0] == "view" or args[0] == "name"):
        # print("entered")
        # we can base the length ALWAYS by the number of tasks
        task_col = (sheet.col_values(1))[2:]
        max_length = len(task_col)
        ppl_resp_col = (sheet.col_values(2))[2:]
        if (len(ppl_resp_col) < max_length):
            for i in range(max_length-len(ppl_resp_col)):
                ppl_resp_col.append('')
        exp_due_date_col = (sheet.col_values(3))[2:]
        if (len(exp_due_date_col) < max_length):
            for i in range(max_length-len(exp_due_date_col)):
                exp_due_date_col.append('')
        completion_col = (sheet.col_values(4))[2:]
        if (len(completion_col) < max_length):
            for i in range(max_length-len(completion_col)):
                completion_col.append('')
        notes_col = (sheet.col_values(5))[2:]
        if (len(notes_col) < max_length):
            for i in range(max_length-len(notes_col)):
                notes_col.append('')

        assert max_length == len(notes_col) == len(completion_col) == len(exp_due_date_col) == len(ppl_resp_col)
        # create dict for pandas conversion
        todo_table = {'Tasks': task_col, 'People Responible': ppl_resp_col, 
            'Expected Due Date': exp_due_date_col, 'Completion Date': completion_col, 'Notes': notes_col}
        # pandas conversion
        todo_df = pd.DataFrame(todo_table)    
        # print(todo_df.to_string())

        # convert df to np to list of rows
        listofdfrows = todo_df.to_numpy().tolist()
        # print(listofdfrows)

        # print(args[1])
        if (args[0] == "view" and (len(args) == 1 or len(args) == 2)):
            if (len(args) == 2):
                adjusted_table = listofdfrows[:int(args[1])]
            else:
                adjusted_table = listofdfrows
            # print(listofdfrows)

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
                        value=f'>People Responsible: {row[1]}\n> Expected Due Date: {row[2]}\n> Completion Date: {row[3]}\n> Notes: {row[4]}',
                        inline=False
                    )
            if (len(embed.fields) == 0):
                embed.add_field (
                    name=f'**No Tasks**',
                    value = f'No Tasks Available for {args[1]}'
                )
            await ctx.channel.send(embed=embed)

    # update the completion date
    elif(args[0] == "complete"):
        if (len(args) != 2):
            await ctx.channel.send("INVALID ARGUMENTS")
            return
        await ctx.channel.send("Command Not Finished")

        print("hi")
    # create new to-do: need name of Task, People Responsible, Due Date
    elif(args[0] == "add"):
        if (len(args) != 5):
            await ctx.channel.send("INVALID ARGUMENTS")
            return
        await ctx.channel.send("Command Not Finished")
            
        print("hi")
    # delete row when to-do is not needed
    elif(args[0] == "delete"):
        if (len(args) != 2):
            await ctx.channel.send("INVALID ARGUMENTS")
            return
        await ctx.channel.send("Command Not Finished")
        
        print("hi")
    else: 
        await ctx.channel.send("BAD ARGUMENTS")




@bot.event
async def on_command_err(ctx,error):
  if isinstance(error, CommandNotFound):
    return
  raise error

# keep_alive()
bot.run(TOKEN)