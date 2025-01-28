import os
from flask import Flask, request, render_template
import spacy

# Initialize the Flask app
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Helper function for POS tagging
def get_pos_tags(text):
    doc = nlp(text)
    return [(token.text, token.pos_) for token in doc]

# Routes
@app.route("/", methods=["GET", "POST"])
def index():
    pos_result = None
    color_map = {
        "NOUN": "lightblue",
        "VERB": "lightgreen",
        "ADJ": "yellow",
        "ADV": "pink",
        "PRON": "orange",
        "CONJ": "lightgray",
        "DET": "beige",
        "PROPN": "violet",
        "INTJ": "lightcoral",
        "NUM": "khaki",
        "PUNCT": "white",
        "X": "cyan",
    }
    text = ""

    if request.method == "POST":
        # If text input is provided
        if "text" in request.form and request.form["text"]:
            text = request.form["text"]
        # If a file is uploaded
        elif "file" in request.files:
            file = request.files["file"]
            if file and file.filename:  # Check if a file is selected
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
                file.save(filepath)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        text = f.read()
                except Exception as e:
                    print("Error reading file:", e)
                    text = "Error reading file content."

        if text:
            pos_result = get_pos_tags(text)

    return render_template("index.html", pos_result=pos_result, color_map=color_map, text=text)

if __name__ == "__main__":
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    app.run(debug=True)
