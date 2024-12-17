from src import Handler
import os, threading, random, webbrowser, json
from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

color = random.choice(["#EE6352", "#746AFE", "#59CD90", "#3FA7D6", "#FAC05E"])


@app.route("/")
def home():
    return render_template("index.html", bg = color)

@app.route("/split")
def split():
    return render_template("split.html", bg = color)

@app.route("/merge")
def merge():
    return render_template("merge.html", bg = color)

@app.route("/from-docx")
def from_docx():
    return render_template("from-docx.html", bg = color)

@app.route("/to-docx")
def to_docx():
    return render_template("to-docx.html", bg = color)


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    metadata = request.form.get("metadata")

    if not metadata:
        return jsonify({"error": "No metadata provided"}), 400

    try:
        metadata = json.loads(metadata)
    except ValueError:
        return jsonify({"error": "invalid metadata format"}), 400

    if file.filename == "":
        return jsonify({"error": "no selected file"}), 400

    if file and str(file.filename).endswith(".pdf"):
        pdf_path = os.path.join(app.config["UPLOAD_FOLDER"], str(file.filename))
        file.save(pdf_path)

        with open(os.path.join(app.config["UPLOAD_FOLDER"], "metadata.json"), "w") as f:
            json.dump(metadata, f, indent=4)

        Handler.handle()

        return jsonify({"message": "upload completed successfully"}), 200
    else:
        return jsonify({"error": "invalid file type"}), 400

def download(filename, directory):
    """Use to send file to the user for download"""
    return send_from_directory(directory, filename, as_attachment=True)


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html", bg = colour), 404

@app.errorhandler(405)
def not_found(error):
    return render_template("405.html", bg = colour), 405


if __name__ == "__main__":
    try:
        print("[  OK  ] Starting app")
        threading.Timer(1, lambda: webbrowser.open('http://127.0.0.1:8080')).start()
        app.run(host="127.0.0.1", port=8080, debug=True)
    except Exception as e:
        print(f"[ FAIL ] Error: {e}")
