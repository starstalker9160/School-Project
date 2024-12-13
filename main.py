import threading
import webbrowser
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

def open_browser():
    webbrowser.open('http://127.0.0.1:8080')

if __name__ == '__main__':
    # threading.Timer(1, open_browser).start()
    app.run(host='127.0.0.1', port=8080, debug=True)
