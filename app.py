from flask import Flask, render_template, jsonify
import csv
import os

app = Flask(__name__)

def read_news():
    news = []
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'news.csv')

    with open(file_path, encoding='utf-8') as f:
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
    app.run(host='0.0.0.0', port=5000, debug=True)
