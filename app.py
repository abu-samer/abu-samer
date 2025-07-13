from flask import Flask, render_template, jsonify
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

app = Flask(__name__)

SERVICE_ACCOUNT_FILE = 'newsupdater-465801-9d1c3cb06279.json'
SPREADSHEET_ID = 'معرف_ملف_الجوجل_شيت_هنا'
SHEET_NAME = 'Sheet1'

def sheets_service():
    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
    )
    service = build('sheets', 'v4', credentials=credentials)
    return service.spreadsheets()

def read_news():
    sheets = sheets_service()
    result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=SHEET_NAME).execute()
    values = result.get('values', [])
    news = []
    for row in values[1:]:  # تخطى العنوان
        if len(row) >= 2:
            news.append(row[1])
    return news

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/news')
def api_news():
    news = read_news()
    return jsonify(news)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
