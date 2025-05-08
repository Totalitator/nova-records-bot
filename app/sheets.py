from datetime import datetime, timedelta
from gspread import Client, Spreadsheet, Worksheet, service_account, utils

gc = service_account(filename='python-sheets-nova-450407-5ccbd0d03bfd.json')

sh = gc.open('Студия-расписание')
wh = sh.get_worksheet(0)

async def check_date(date) -> str:
    date_cell = Worksheet.find(self=wh, query=date, in_column=1)
    if date_cell is None:
        return 'Указана неверная дата'

    row_values = wh.row_values(date_cell.row)
    search_word = 'Забронировано'
    count = 0
    
    for value in row_values:
        if value == search_word:
            count+= 1

    if count == 11:
        return 'На этот день нет свободных мест'
    
    return None


async def check_time(date, start) -> str:
    date_cell = Worksheet.find(self=wh, query=date, in_column=1)
    start_cell = Worksheet.find(self=wh, query=start, in_row=1)

    if start == '13:00':
        return 'Обед! В это время мы подкрепляемся и восстанавливаем силы.'

    start_cross_cell = Worksheet.cell(self=wh, row=date_cell.row, col=start_cell.col)

    if start_cross_cell.value == 'Забронировано':
        return 'К сожалению, это время уже забронировала будущая рок-звезда.'

    return None

async def check_hours(date, start, hours):
    print(hours)
    if hours is None:
        return 'ну че блять', 0, 0, 0
    date_cell = Worksheet.find(self=wh, query=date)
    start_cell = Worksheet.find(self=wh, query=start)

    end = await convert_time(start, hours)
    end_cell = Worksheet.find(self=wh, query=end)

    range_row = wh.row_values(date_cell.row)
    values = range_row[start_cell.col:end_cell.col]

    for value in values:
        if value != 'v':
            return value, 0, 0, 0

    return None, date_cell.row, start_cell.col, end_cell.col

async def convert_time(start, hours) -> str:
    start_hour = datetime.strptime(start, "%H:%M")
    end_hour = start_hour + timedelta(hours=float(hours))
    return end_hour.strftime("%H:%M")

async def booking_cells(date_row, start_col, end_col):
    print(date_row)
    range_row = wh.row_values(date_row)
    values = range_row[start_col:end_col+1]
    for idx, value in enumerate(values):
        if value == 'v':
            wh.update_cell(date_row, start_col+idx, 'Забронировано')
            wh.update_cell(date_row, end_col+1, 'Резерв')