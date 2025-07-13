import os
import json
from flask import Flask, render_template, jsonify, request
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import time

app = Flask(__name__)

SERVICE_ACCOUNT_INFO = os.getenv('GOOGLE_CREDENTIALS_JSON')
SPREADSHEET_ID = '1kNO7lNC5uC9PYRsE-vk8OZypQxnbZFI0evOVfWYdGsE'
SHEET_NAME = 'Sheet1'

cached_news = []
last_update_time = 0

def sheets_service():
    credentials = Credentials.from_service_account_info(
        json.loads(SERVICE_ACCOUNT_INFO),
        scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
    )
    service = build('sheets', 'v4', credentials=credentials)
    return service.spreadsheets()

def update_news_cache():
    global cached_news, last_update_time
    sheets = sheets_service()
    result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=SHEET_NAME).execute()
    values = result.get('values', [])
    news = []
    for row in values[1:]:
        if len(row) >= 2:
            news.append(row[1])
    cached_news = news
    last_update_time = time.time()
    print(f"News cache updated at {time.ctime(last_update_time)}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/news')
def api_news():
    if not cached_news:
        return jsonify({"error": "News not loaded yet. Please trigger update first."}), 503
    return jsonify(cached_news)

@app.route('/update_news', methods=['POST'])
def update_news():
    # ممكن تضيف تحقق للتأكد انه الطلب من مصدر موثوق (مثلاً تحقق من توكن أو مفتاح)
    update_news_cache()
    return jsonify({"status": "News cache updated successfully"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
