from flask import Flask, render_template, jsonify
import csv
import threading
import asyncio
asyncio.run(update_news())
import update_news  # استورد ملفك الجديد

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

def run_updater():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(update_news.update())

if __name__ == '__main__':
    # شغل التحديث في خيط مستقل
    updater_thread = threading.Thread(target=run_updater, daemon=True)
    updater_thread.start()

    app.run(host='0.0.0.0', port=5000)
