import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

scope =  ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("Official Python Project-6c3e70b9c89c.json", scope)

client = gspread.authorize(creds)

sheet =  client.open("test").sheet1  #can do sheet2,3,etc

data = sheet.get_all_records()


row = sheet.row_values(1)

sheet.insert_row(["1", "sakura liu", "markus paolo"],6)
sheet.update_cell(5,7, "this is pretty sick to be honest")
pprint(data)

pprint(row)  #print is regular print not as nice, pprint = pretty print
