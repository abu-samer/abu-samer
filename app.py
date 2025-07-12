from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/news')
def get_news():
    return jsonify([
        "🔴 عاجل: هذا خبر تجريبي",
        "🟢 جديد: هذا خبر ثاني",
        "🟡 مهم: هذا خبر ثالث"
    ])

if __name__ == '__main__':
    app.run(host='0.0.0.0')
