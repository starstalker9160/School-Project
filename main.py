from random import choice
from threading import Timer
from json import dump, loads
from src import Handler, colors
from webbrowser import open as webbrowser_open
from os import path, remove, rmdir, makedirs, walk
from json import dump, loads
from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    send_from_directory,
    url_for,
    redirect,
)

#* Initializing the Flask app
app = Flask(__name__)
"""The Flask app object, used to initialize the web server."""

UPLOAD_FOLDER = "uploads"
"""Path for the 'uploads' folder, relative to the current working directory."""

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
"""Random color chosen for the background of the web pages\n
3000 possible options of color can be chosen"""


@app.route("/")
def home():
    """The route for the home page of the web app."""
    return render_template("index.html", bg=color)


@app.route("/split")
def split():
    """The route for the split page of the web app."""
    return render_template("split.html", bg=color)


@app.route("/merge")
def merge():
    """The route for the merge page of the web app."""
    return render_template("merge.html", bg=color)


@app.route("/error")
def error_page():
    """The route for the error page of the web app.\n
    This error page is used to display any error that occurs STRICTLY during the any PDF operation."""

    error_message = request.args.get("error_message", "Unknown error occurred")
    return render_template("error.html", error_data={"color": color, "error_message": error_message})


@app.route("/upload", methods=["POST"])
def upload_file():
    """The route for the file upload endpoint.\n
    This endpoint is used to upload the files and metadata to the server."""

    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    files = request.files.getlist("file") #* Getting the files from the request
    metadata = request.form.get("metadata") #* Getting the metadata from the request

    if not metadata:
        #* If no metadata is provided, return an error, since metadata is required for every operation
        return jsonify({"error": "No metadata provided"}), 400

    try:
        #* Make sure that metadata is of correct format
        metadata = loads(metadata)
    except ValueError:
        print(metadata) #* Printing invalid metadata for debugging purposes
        return jsonify({"error": "Invalid metadata format"}), 400

    if not files:
        #* If no files are provided, return an error, since files are required for every operation
        return jsonify({"error": "No files selected"}), 400

    allowedExts = {".pdf"} #* Conversion is only possible between PDFs, thus the only allowed extension is .pdf
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

            try:
                i.save(file_path)
                uploaded_files.append(file_path)
            except OSError:
                return jsonify({"error": "Failed to save file"}), 500

    with open(path.join(app.config["UPLOAD_FOLDER"], "metadata.json"), "w") as f:
        dump(metadata, f, indent=4) #* Serializing the metadata to a JSON file

    try:
        Handler.handle() #* Begin the PDF operation
        return jsonify({"message": "Operation completed successfully."}), 200
    except Exception as e:
        #! In case of any exception, trigger the error page to display the error to the user
        return redirect(url_for("error_page", error_message=str(e), color=color))


def download(filename, directory):
    """Used to send a file to the user for download."""
    return send_from_directory(directory, filename, as_attachment=True)


@app.errorhandler(404)
def not_found_404(error):
    """The error handler for 404 errors."""
    return render_template("404.html", bg=color), 404


@app.errorhandler(405)
def not_found_405(error):
    """The error handler for 405 errors."""
    return render_template("405.html", bg=color), 405


#* Main function to start the app
if __name__ == "__main__":
    try:
        print("[  OK  ] Starting app")
        Timer(1, lambda: webbrowser_open("http://127.0.0.1:8080")).start()
        app.run(host="127.0.0.1", port=8080, debug=True)
    except Exception as e:
        print(f"[ FAIL ] Error: {e}")
