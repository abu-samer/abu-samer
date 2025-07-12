from flask import Flask, render_template, jsonify
import csv
import os

app = Flask(__name__)

def read_news():
    news = []
    with open('news.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            news.append(row['message'])
    return news

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/news')
def api_news():
    news = read_news()
    return jsonify(news)

if __name__ == '__main__':
    print("🔵 Flask شغّال...")

    # اعدادات التشغيل للسيرفر
    port = int(os.environ.get('PORT', 5000))  # يستقبل رقم البورت من بيئة التشغيل أو 5000
    app.run(host='0.0.0.0', port=port)  # لا تضع debug=True في السيرفر الحقيقي
