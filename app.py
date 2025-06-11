from flask import Flask, render_template, request, redirect
import os
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)
DATA_FILE = 'static/data/mrn_data.json'
UPLOAD_FOLDER = 'static/data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    query = request.form.get("mrn", "").strip().upper()
    results = []

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            for item in data:
                if item.get("MRN", "").upper() == query:
                    results.append(item)

    return render_template("index.html", results=results, query=query)

@app.route("/admin", methods=["POST"])
def admin_upload():
    username = request.form.get("username")
    password = request.form.get("password")
    if username == "21579" and password == "14419907690":
        file = request.files.get("file")
        if file and file.filename.endswith(".json"):
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(file.filename))
            file.save(filepath)
            os.replace(filepath, DATA_FILE)
            return redirect("/")
    return redirect("/")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
