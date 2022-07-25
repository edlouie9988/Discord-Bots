from unicodedata import name
import gspread

def get_info(spreadsheet_name):
    # get service account based on ~/.config/gspread
    sa = gspread.service_account(filename="service_account.json")

    # open Google Sheet file by name
    spreadsheet = sa.open("FVE 2022-2023 Logistics")

    # access particular sheet within file, specified by user
    if (spreadsheet_name == "comp"):
        sheet = spreadsheet.worksheet("Comp Team Roster")
    elif (spreadsheet_name == "gen"):
        sheet = spreadsheet.worksheet("Gen Member Roster")
    else:
        return None,None

    '''
    Data needed to be accessed:
    [First Name (A), Last Name(B), Discord ID(D)]
    '''
    first_names_arr = sheet.col_values(1)
    last_names_arr = sheet.col_values(2)
    discord_id_arr = sheet.col_values(4)
    discord_id_arr = discord_id_arr[1:]
    
    for i in range(len(discord_id_arr)):
        discord_id_arr[i] = discord_id_arr[i][:len(discord_id_arr[i])-5]

    first_names_arr = first_names_arr[1:]
    last_names_arr = last_names_arr[1:]
    

    # combine first and last name
    name_arr = []
    for i in range(len(first_names_arr)):
        temp_str = first_names_arr[i] + " " + last_names_arr[i]
        name_arr.append(temp_str)
        
    return name_arr, discord_id_arr