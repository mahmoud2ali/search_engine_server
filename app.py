from flask import Flask, request, jsonify
from pyngrok import ngrok
from flask_cors import CORS
from pymongo.server_api import ServerApi
import random
import math
from pyngrok import ngrok
from helper import *
from retriving import search



app = Flask(__name__)


CORS(app)



@app.route('/')
def retrive_random_books():
    random_books = get_random_books()

    # Process each book
    for book in random_books:
        for key, value in book.items():
            if value is None or value == "NaN" or (isinstance(value, float) and pd.isna(value)):
                book[key] = 0  # Or any placeholder

    return jsonify(random_books)



@app.route('/embed', methods=['POST'])
def embed():
    try:
        data = request.json
        text = data.get("text", "")
        genre = data.get("genre", None)  # Optional: support genre filtering

        results = search(text, genre)

        if results:
            return jsonify(results), 200
        else:
            return jsonify({"message": "⚠️ لم يتم العثور على نتائج"}), 404
        
    except Exception as e:
        print("Data: ",data)
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500
    
    

if __name__  == "__main__":
    # public_url = ngrok.connect(5000, domain="manatee-allowed-nominally.ngrok-free.app")
    # print(" * ngrok tunnel:", public_url)

    # Start Flask app
    app.run(debug=False, port=5000)