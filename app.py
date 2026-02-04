from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# CSV file ka naam (Ensure GitHub pe yahi naam ho)
FILE_NAME = 'aadhar(1).xlsx - Sheet1.csv'

def load_data():
    if os.path.exists(FILE_NAME):
        try:
            # CSV load kar rahe hain strings ki tarah
            df = pd.read_csv(FILE_NAME, dtype=str)
            return df
        except Exception as e:
            return None
    return None

df = load_data()

@app.route('/')
def home():
    return jsonify({
        "status": "System Online",
        "owner": "ARYAN",
        "usage": "/search?num=your_number"
    })

@app.route('/search')
def api_search():
    num_query = request.args.get('num', '').strip()
    
    if not num_query:
        return jsonify({"error": "Provide 'num' parameter", "developer": "ARYAN"}), 400

    if df is None:
        return jsonify({"error": "Database not found", "developer": "ARYAN"}), 500

    # phoneNumber column mein search
    results = df[df['phoneNumber'].str.contains(num_query, na=False)]

    if results.empty:
        return jsonify({
            "SUCCESS": False,
            "results": [], 
            "count": 0, 
            "developer": "ARYAN"
        })

    return jsonify({
        "SUCCESS": True,
        "results": results.to_dict(orient="records"),
        "count": len(results),
        "developer": "ARYAN"
    })
