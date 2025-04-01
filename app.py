from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os

app = Flask(__name__)

DATA_FILE = "hsr_characters.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

@app.route("/")
def index():
    characters = load_data()
    characters_with_index = list(enumerate(characters))  # Voeg de index toe aan de lijst
    return render_template("index.html", characters=characters_with_index)

@app.route("/add", methods=["GET", "POST"])
def add_character_page():
    if request.method == "POST":
        name = request.form.get("name")
        char_type = request.form.get("type")
        path = request.form.get("path")
        characters = load_data()
        characters.append({"name": name, "type": char_type, "path": path})
        save_data(characters)
        return redirect(url_for("index"))
    return render_template("add.html")

@app.route("/characters", methods=["GET"])
def get_characters():
    return jsonify(load_data())

@app.route("/characters", methods=["POST"])
def add_character():
    data = request.json
    characters = load_data()
    characters.append({"name": data["name"], "type": data["type"], "path": data["path"]})
    save_data(characters)
    return jsonify({"message": "Character added successfully"}), 201

@app.route("/characters/<int:index>", methods=["PUT"])
def update_character(index):
    characters = load_data()
    if 0 <= index < len(characters):
        data = request.get_json()  # Gebruik request.get_json() om JSON-gegevens te verwerken
        characters[index] = {
            "name": data["name"], 
            "type": data["type"], 
            "path": data["path"]
        }
        save_data(characters)
        return jsonify({"message": "Character updated successfully"})
    return jsonify({"error": "Character not found"}), 404

@app.route("/characters/<int:index>", methods=["DELETE"])
def delete_character(index):
    characters = load_data()
    if 0 <= index < len(characters):
        del characters[index]
        save_data(characters)
        return jsonify({"message": "Character deleted successfully"})
    return jsonify({"error": "Character not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)