import gspread
from bs4 import BeautifulSoup

import requests

password = raw_input("Enter tunabrix password: ")

gc = gspread.login('tunabrix@gmail.com', password)

last_file = open("previous_spreadsheet.txt", "r+")
previous_spreadsheet = str(last_file.readline())

print "Previous stored spreadsheet: "+previous_spreadsheet

r  = requests.get("http://musical.epfl.ch")

data = r.text

soup = BeautifulSoup(data)

print "Start process"

spreadsheetlinks = []
for link in soup.find_all('a'):
    if str(link.get('href')).startswith('http://docs.google.com'):                            
        spreadsheetlinks.append(link.get('href'))

print spreadsheetlinks

#if len(spreadsheetlinks) is not 4:
#    raise("There are more than 4 spreadsheets on the page. Aborting for safety")

newest_spreadsheet = spreadsheetlinks[-1]

if previous_spreadsheet == str(newest_spreadsheet):
    print "No new spreadsheet. Finishing"
else:
    print "Spreadsheet that will change:"
    print newest_spreadsheet
    
    spreadsheet = gc.open_by_url(newest_spreadsheet)
    
    worksheet = spreadsheet.sheet1
    
    cell_list = worksheet.range('D21:D23')
    
    for cell in cell_list:
        if cell.value == '':
            cell.value = 'TunaBrix!'
    
    worksheet.update_cells(cell_list)
    
    last_file.write(str(newest_spreadsheet)) 

print "Job's Done. See ya!"
