from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/news')
def get_news():
    return jsonify([
        "هذا خبر تجريبي 🔥",
        "خبر ثاني 🚀",
        "خبر ثالث 🎉"
    ])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
