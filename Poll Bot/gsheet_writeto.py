import gspread

def write_data_to_sheet(yes_arr, no_arr, date_str):
    SPREADSHEET_NAME = "Comp Team Attendance"
    # get service account based on ~/.config/gspread
    sa = gspread.service_account(filename="service_account.json")

    # open Google Sheet file by name
    spreadsheet = sa.open("FVE 2022-2023 Logistics")

    sheet = spreadsheet.worksheet(SPREADSHEET_NAME)

    # find next empty column
    i = 1
    for i in range(1,100):
        if (len(sheet.col_values(i)) == 0):
            break
    col = i
    sheet.update_cell(1, col, date_str)    

    first_name_arr = sheet.col_values(1)
    last_names_arr = sheet.col_values(2)

    # parse yes_arr data
    first_name = ''
    last_name = ''
    for name in yes_arr:
        first_name = name.split(" ")[0]
        last_name = name.split(" ")[1]
        if (first_name in first_name_arr and last_name in last_names_arr):
            row = first_name_arr.index(first_name) + 1
            sheet.update_cell(row, col, "Yes")

    # parse no_arr data
    for name in no_arr:
        first_name = name.split(" ")[0]
        last_name = name.split(" ")[1]
        if (first_name in first_name_arr and last_name in last_names_arr):
            row = first_name_arr.index(first_name) + 1
            sheet.update_cell(row, col, "No")

    return