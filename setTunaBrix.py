import gspread
from bs4 import BeautifulSoup

import requests

password = raw_input("Enter tunabrix password: ")

gc = gspread.login('tunabrix@gmail.com', password)

last_file = open("last_spreadsheet.txt", "r+")
last_spreadsheet = str(last_file.readline())

print "Last spreadsheet: "+last_spreadsheet

r  = requests.get("http://musical.epfl.ch")

data = r.text

soup = BeautifulSoup(data)

print "Start process"

spreadsheetlinks = []
for link in soup.find_all('a'):
    if str(link.get('href')).startswith('http://docs.google.com'):                            
        spreadsheetlinks.append(link.get('href'))

print spreadsheetlinks

if len(spreadsheetlinks) is not 4:
    raise("There are more than 4 spreadsheets on the page. Aborting for safety")

if last_spreadsheet == str(spreadsheetlinks[3]):
    print "No new spreadsheet. Finishing"
else:
    print "Spreadsheet that will change:"
    print spreadsheetlinks[3]
    
    spreadsheet = gc.open_by_url(spreadsheetlinks[3])
    
    worksheet = spreadsheet.sheet1
    
    cell_list = worksheet.range('D21:D23')
    
    for cell in cell_list:
        if cell.value == '':
            cell.value = 'TunaBrix!'
    
    worksheet.update_cells(cell_list)
    
    last_file.write(str(spreadsheetlinks[3])) 

print "Job's Done. See ya!"
