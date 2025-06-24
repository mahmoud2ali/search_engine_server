from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import random
import math


app = Flask(__name__)

CORS(app)

model = SentenceTransformer('./model')

uri = "mongodb+srv://admin-mahmoud:0123456789@cluster0.8w33a.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


db = client['books_dataset']
collection = db['books']

books = list(collection.find())


@app.route('/')
def get_random_books():
    # Retrieve 10 random books using MongoDB's aggregation pipeline
    random_books = list(collection.aggregate([{"$sample": {"size": 10}}]))

    # Process each book
    for book in random_books:
        book['_id'] = str(book['_id'])

        for book in random_books:
            for key, value in book.items():
                if value is None or value == "NaN":
                    book[key] = 0
                elif isinstance(value, float) and math.isnan(value):
                    book[key] = 0

    return jsonify(random_books)



@app.route('/embed', methods=['POST'])
def embed():
    try:
        data = request.json
        print("Received data:", data)
        text = data.get("text", "")
        embedding = model.encode(text).tolist()
        return jsonify({"embedding": embedding})
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500



if __name__  == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)