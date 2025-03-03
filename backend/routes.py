from flask import render_template, request, redirect, url_for
import os
import pandas as pd
from XMLParse import parse_xml_to_csv

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def setup_routes(app):
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/checklist")
    def checklist():
        return render_template("checklist.html")

    @app.route("/progress")
    def progress():
        return render_template("progress.html")

    @app.route("/upload", methods=["GET", "POST"])
    def upload_file():
        if request.method == "POST":
            if "file" not in request.files:
                return "No file part"
            file = request.files["file"]
            if file.filename == "":
                return "No selected file"
            if file and file.filename.endswith(".des"):
                filepath = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(filepath)
                parse_xml_to_csv(filepath, PROCESSED_FOLDER)
                return redirect(url_for("index"))
        return render_template("upload.html")
