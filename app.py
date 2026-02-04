from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# Sabse pehle file dhoondne ka logic
def get_csv_file():
    # Jo tune file upload ki hai uska exact naam yaha likho
    possible_names = ['aadhar(1).xlsx - Sheet1.csv', 'data.csv', 'aadhar.csv']
    for name in possible_names:
        if os.path.exists(name):
            return name
    return None

FILE_NAME = get_csv_file()

def load_data():
    if FILE_NAME:
        try:
            return pd.read_csv(FILE_NAME, dtype=str)
        except:
            return None
    return None

df = load_data()

@app.route('/')
def home():
    return jsonify({"status": "Online", "file_found": FILE_NAME is not None, "owner": "ARYAN"})

@app.route('/search')
def api_search():
    num_query = request.args.get('num', '').strip()
    if not num_query:
        return jsonify({"error": "Num missing"}), 400

    if df is None:
        return jsonify({"developer": "ARYAN", "error": "Database not found", "debug": "Check file name on GitHub"}), 500

    # phoneNumber column mein search
    results = df[df['phoneNumber'].str.contains(num_query, na=False)]

    return jsonify({
        "SUCCESS": True if not results.empty else False,
        "results": results.to_dict(orient="records"),
        "developer": "ARYAN"
    })
