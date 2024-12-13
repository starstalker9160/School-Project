import threading, random, webbrowser
from flask import Flask, render_template

app = Flask(__name__)

colour = random.choice(["#EE6352", "#746AFE", "#59CD90", "#3FA7D6", "#FAC05E"])

@app.route('/')
def home():
    return render_template('index.html', bg = colour)

@app.route('/split')
def split():
    return render_template('split.html', bg = colour)

@app.route('/merge')
def merge():
    return render_template('merge.html', bg = colour)

@app.route('/from-docx')
def from_docx():
    return render_template('from-docx.html', bg = colour)

@app.route('/to-docx')
def to_docx():
    return render_template('to-docx.html', bg = colour)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', bg = colour), 404

if __name__ == '__main__':
    try:
        print("[  OK  ] Starting app")
        # threading.Timer(1, lambda: webbrowser.open('http://127.0.0.1:8080')).start()
        app.run(host='127.0.0.1', port = 8080, debug = True)
        print("[  OK  ] App started")
    except Exception as e:
        print(f"[ FAIL ] Error: {e}")
