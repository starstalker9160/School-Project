from src import Handler, colors
from os import path, remove, rmdir, makedirs, walk
from random import choice
from threading import Timer
from json import dump, loads
from webbrowser import open as webbrowser_open
from json import dump, loads
from flask import Flask, render_template, request, jsonify, send_from_directory, url_for, redirect

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
if path.exists(UPLOAD_FOLDER):
    for r, d, f in walk(UPLOAD_FOLDER, topdown=False):
        for file in f:
            remove(path.join(r, file))
        for dir in d:
            rmdir(path.join(r, dir))
    rmdir(UPLOAD_FOLDER)
makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
color = choice(colors.colors)


@app.route("/")
def home():
    return render_template("index.html", bg=color)


@app.route("/split")
def split():
    return render_template("split.html", bg=color)


@app.route("/merge")
def merge():
    return render_template("merge.html", bg=color)


@app.route("/error")
def error_page():
    error_message = request.args.get("error_message", "Unknown error occurred")
    return render_template("error.html", error_data={"color": color, "error_message": error_message})


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    files = request.files.getlist("file")
    metadata = request.form.get("metadata")

    if not metadata:
        return jsonify({"error": "No metadata provided"}), 400

    try:
        metadata = loads(metadata)
    except ValueError:
        print(metadata)
        return jsonify({"error": "Invalid metadata format"}), 400

    if not files:
        return jsonify({"error": "No files selected"}), 400

    allowedExts = {".pdf"}
    for i in files:
        if i.filename == "":
            return jsonify({"error": "No selected file"}), 400

        if i.filename is None:
            return jsonify({"error": "File name is None"}), 400
        ext = path.splitext(i.filename)[1].lower()
        if ext not in allowedExts:
            return jsonify({"error": f"Invalid file type for {i.filename}"}), 400

    uploaded_files = []
    for i in files:
        name = i.filename
        if name is not None:
            file_path = path.join(app.config["UPLOAD_FOLDER"], name)

            i.save(file_path)
            uploaded_files.append(file_path)

    with open(path.join(app.config["UPLOAD_FOLDER"], "metadata.json"), "w") as f:
        dump(metadata, f, indent=4)

    try:
        Handler.handle()
        return jsonify({"message": "Operation completed successfully."}), 200
    except Exception as e:
        return redirect(url_for("error_page", error_message=str(e), color=color))


def download(filename, directory):
    """Use to send file to the user for download"""
    return send_from_directory(directory, filename, as_attachment=True)


@app.errorhandler(404)
def not_found_404(error):
    return render_template("404.html", bg=color), 404


@app.errorhandler(405)
def not_found_405(error):
    return render_template("405.html", bg=color), 405


if __name__ == "__main__":
    try:
        print("[  OK  ] Starting app")
        Timer(1, lambda: webbrowser_open("http://127.0.0.1:8080")).start()
        app.run(host="127.0.0.1", port=8080, debug=False)
    except Exception as e:
        print(f"[ FAIL ] Error: {e}")
