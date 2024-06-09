import json
import os

from flask import Flask, make_response, request

app = Flask(__name__)

import gspread
from oauth2client.service_account import ServiceAccountCredentials


@app.route('/')
def index():
    return 'Submit post requests to /addRow'

@app.route('/addRow', methods=['POST', 'OPTIONS'])
def add():
    data = request.get_json()

    if request.method == 'OPTIONS':
        response = make_response("Success", 200)
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', '*')
        response.headers.add('Access-Control-Allow-Methods', '*')
        return response

    password = data['password'] if 'password' in data else None
    if password != os.environ.get('PASSWORD'):
        return make_response("Unauthorized", 401)

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = json.loads(os.environ.get('GOOGLE_CREDS'))
    with open('/tmp/gcreds.json', 'w') as f:
        json.dump(creds, f)
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        '/tmp/gcreds.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open("Regnskap")

    worksheet = sheet.worksheet("Utgifter 2024")
    
    new_row = [data['date'], data['date'], data['amount'], data['description'], data['category'], data['tag']]
    worksheet.append_row(new_row, value_input_option='USER_ENTERED')
    response = make_response("Success", 200)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', '*')
    return response