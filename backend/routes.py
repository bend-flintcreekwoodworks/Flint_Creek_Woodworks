import os
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, flash
from XMLParse import parse_xml_to_csv

UPLOAD_FOLDER = "backend/uploads"
PROCESSED_FOLDER = "backend/processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def setup_routes(app):
    # Set upload folder in app config
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    app.config["SECRET_KEY"] = "your_secret_key"  # Required for flash messages

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
                flash("No file part", "error")
                return redirect(url_for("upload_file"))

            file = request.files["file"]
            if file.filename == "":
                flash("No selected file", "error")
                return redirect(url_for("upload_file"))

            if file and file.filename.endswith(".des"):
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
                
                try:
                    file.save(filepath)
                    parse_xml_to_csv(filepath, PROCESSED_FOLDER)
                    flash(f"File {file.filename} uploaded and processed successfully!", "success")
                    return redirect(url_for("index"))
                except Exception as e:
                    flash(f"Error processing file: {str(e)}", "error")
                    return redirect(url_for("upload_file"))

            flash("Invalid file type. Only .des files allowed.", "error")
            return redirect(url_for("upload_file"))

        return render_template("upload.html")
