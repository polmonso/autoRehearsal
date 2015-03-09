import gspread
from bs4 import BeautifulSoup

import sys
import requests

import os
dir_name = os.path.dirname(__file__)

last_spreadsheet_file = os.path.join(dir_name, "previous_spreadsheet.txt")

with open(os.path.join(dir_name, 'account'), 'r') as f:
    email = f.readline()
    password = f.readline()

    gc = gspread.login(email, password)

# password = raw_input("Enter tunabrix password: ")

try:
    with open(last_spreadsheet_file, "r") as f:
        previous_spreadsheet = str(f.readline())
except IOError:
    previous_spreadsheet = ''

print "Previous stored spreadsheet: "+previous_spreadsheet

r  = requests.get("http://musical.epfl.ch")

data = r.text

soup = BeautifulSoup(data)

print "Start process"

spreadsheetlinks = []
for link in soup.find_all('a'):
    link_url = link.get('href')
    if '://docs.google.com' in link_url:
        s_key = link_url.split("/")[-1]
        if s_key == '':
            s_key = link_url.split("/")[-2]
        spreadsheetlinks.append(str(s_key))

print "Found the following links:"
print spreadsheetlinks

# Find out whether the last spreadsheet we modified
# is one of the spreadsheets we found.

try:
    # If that's the case,
    #  we're going to begin from the spreadsheet
    # after the one we last modified
    start_index = spreadsheetlinks.index(previous_spreadsheet) + 1
except ValueError:
    # Otherwise, we start from the very beginning
    start_index = 0

for link in spreadsheetlinks[start_index:]:
    print "Spreadsheet that will change:"
    print link

    spreadsheet = gc.open_by_key(link)

    worksheet = spreadsheet.sheet1

    cell_list = worksheet.range('D21:D23')

    for cell in cell_list:
        old_value = cell.value
        if cell.value == '':
            cell.value = 'Tuna Brix'
        new_value = cell.value
        print old_value, '->', new_value

    worksheet.update_cells(cell_list)

try:
    with open(last_spreadsheet_file, "w") as f:
        newest_spreadsheet = spreadsheetlinks[-1]
        f.write(str(newest_spreadsheet))
except IOError:
    pass

print "Job's Done. See ya!"
