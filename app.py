import os
import json
import time
from flask import Flask, render_template, jsonify
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

app = Flask(__name__)

# نص JSON محفوظ في متغير بيئي (Environment Variable)
SERVICE_ACCOUNT_INFO = os.getenv('GOOGLE_CREDENTIALS_JSON')
SPREADSHEET_ID = '1kNO7lNC5uC9PYRsE-vk8OZypQxnbZFI0evOVfWYdGsE'
SHEET_NAME = 'Sheet1'

# متغيرات الكاش
cached_news = None
last_update_time = 0
CACHE_DURATION = 2  # 300 ثانية = 5 دقائق

def sheets_service():
    credentials = Credentials.from_service_account_info(
        json.loads(SERVICE_ACCOUNT_INFO),
        scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
    )
    service = build('sheets', 'v4', credentials=credentials)
    return service.spreadsheets()

def fetch_news():
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
    global cached_news, last_update_time
    current_time = time.time()
    
    # إذا ما فيه كاش أو انتهى وقت الكاش يحدث البيانات
    if cached_news is None or (current_time - last_update_time) > CACHE_DURATION:
        try:
            new_news = fetch_news()
            cached_news = new_news
            last_update_time = current_time
        except Exception as e:
            # إذا صار خطأ بالإتصال أو غيره، نرجع الكاش القديم لو موجود
            if cached_news is None:
                return jsonify({'error': 'Failed to fetch news'}), 500
    
    return jsonify(cached_news)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
