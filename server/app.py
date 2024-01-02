import os
import json
from flask import (
    Flask,
    request,
    make_response,
)

app = Flask(__name__)

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = json.loads(os.environ['GOOGLE_CREDS'])
with open('gcreds.json', 'w') as f:
    json.dump(creds, f)
creds = ServiceAccountCredentials.from_json_keyfile_name(
    'gcreds.json', scope)
client = gspread.authorize(creds)

sheet = client.open("Regnskap")

worksheet = sheet.worksheet("Utgifter 2024")

@app.route('/addRow', methods=['POST'])
def add():
    data = request.get_json()
    new_row = [data['date'], data['date'], data['amount'], data['description'], data['category']]
    worksheet.append_row(new_row, value_input_option='USER_ENTERED')
    return make_response("OK", 200)