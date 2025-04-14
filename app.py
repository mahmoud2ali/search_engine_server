from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from transformers import AutoTokenizer, AutoModel 
# from tensorflow.keras.models import load_model
import random
import math

from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('./model')




app = Flask(__name__)
CORS(app)


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






@app.route('/search/<query>/', defaults={'category': None}, methods=['POST'])
@app.route('/search/<query>/<category>', methods=['POST'])
def search(query, category):
    data = request.get_json()
    query = data.get("query", "")

    Generate embedding for the query
    query_embedding = model.encode(query, convert_to_tensor=True)

    Compute cosine similarity
    scores = util.cos_sim(query_embedding, book_embeddings)[0].cpu().numpy()
    top_indices = np.argsort(scores)[::-1][:10]

    Get the top books based on similarity
    top_books = [books[i] for i in top_indices]

    return jsonify(top_books)


if __name__  == "__main__":
    app.run(debug = True)