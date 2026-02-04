from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# Jo naam tumne bataya, wahi yahan likh diya hai
FILE_NAME = 'aadhar(1).xlsx - Sheet1.csv'

def load_data():
    if os.path.exists(FILE_NAME):
        try:
            # CSV read kar rahe hain
            df = pd.read_csv(FILE_NAME, dtype=str)
            # Column names ke extra space khatam karne ke liye
            df.columns = df.columns.str.strip()
            return df
        except Exception as e:
            return None
    return None

df = load_data()

@app.route('/')
def home():
    file_status = "Found" if os.path.exists(FILE_NAME) else "Not Found"
    return jsonify({
        "status": "Online",
        "database_file": file_status,
        "owner": "ARYAN"
    })

@app.route('/search')
def api_search():
    num_query = request.args.get('num', '').strip()
    
    if not num_query:
        return jsonify({"SUCCESS": False, "error": "Number missing"}), 400

    if df is None:
        return jsonify({
            "SUCCESS": False, 
            "error": "Database not found",
            "check_file": FILE_NAME
        }), 500

    # Search in phoneNumber column
    # contains() use kiya hai taaki agar number ke aage peeche space ho toh bhi mil jaye
    results = df[df['phoneNumber'].str.contains(num_query, na=False)]

    if results.empty:
        return jsonify({"SUCCESS": False, "results": [], "msg": "No record found"})

    return jsonify({
        "SUCCESS": True,
        "results": results.to_dict(orient="records"),
        "developer": "ARYAN"
    })
