import threading
import webbrowser
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/split')
def split():
    return render_template('split.html')

@app.route('/merge')
def merge():
    return render_template('merge.html')

if __name__ == '__main__':
    try:
        print("[  OK  ] Starting app")
        threading.Timer(1, lambda: webbrowser.open('http://127.0.0.1:8080')).start()
        app.run(host='127.0.0.1', port=8080, debug=True)
        print("[  OK  ] App started")
    except Exception as e:
        print(f"[ FAIL ] Error: {e}")
