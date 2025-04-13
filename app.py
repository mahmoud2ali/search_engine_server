from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# from sentence_transformers import SentenceTransformer, util
import numpy as np

app = Flask(__name__)
CORS(app)

# MongoDB setup
# client = MongoClient("mongodb://localhost:27017/")

# client = MongoClient("mongodb+srv://admin-mahmoud:0123456789@cluster0.8w33a.mongodb.net/")



uri = "mongodb+srv://admin-mahmoud:0123456789@cluster0.8w33a.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


db = client['books_dataset']
collection = db['books']

# Precompute embeddings for all books in MongoDB (this can be done on the fly, but for optimization, precompute)
books = list(collection.find())
# book_embeddings = model.encode([book['description'] for book in books], convert_to_tensor=True)


@app.route('/')
def index():
    return "hello, world!"


@app.route('/books', methods=['GET'])
def get_books():
    # Retrieve the first 10 books from MongoDB
    books = list(collection.find().limit(10))

    # Convert ObjectId to string for JSON response
    for book in books:
        book['_id'] = str(book['_id'])

    return jsonify(books)

# @app.route('/search', methods=['POST'])
# def search():
#     # data = request.get_json()
#     # query = data.get("query", "")

#     # Generate embedding for the query
#     # query_embedding = model.encode(query, convert_to_tensor=True)

#     # Compute cosine similarity
#     # scores = util.cos_sim(query_embedding, book_embeddings)[0].cpu().numpy()
#     # top_indices = np.argsort(scores)[::-1][:10]

#     # Get the top books based on similarity
#     # top_books = [books[i] for i in top_indices]

#     return jsonify(top_books)


if __name__  == "__main__":
    app.run(debug = True)