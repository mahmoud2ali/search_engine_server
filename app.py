from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
# from tensorflow.keras.models import load_model
#from sklearn.metrics.pairwise import cosine_similarity
import random
import math

# from sentence_transformers import SentenceTransformer
# import numpy as np

# model = SentenceTransformer('./model')




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


#for post request
##########---------#############

# @app.route('/search', methods=['POST'])
# def search():
#     data = request.get_json() #  query and category as JSON (flutter send).
    
#     query = data.get("query", "")

#     category = data.get("category", None)  # this can be None or a default

#     if not query:
#         return jsonify({"error": "Query is required"}), 400 

#     ########## preprocessing code #################





#     #########################################


#     # embed the query
#     query_embedding = model.encode([query])[0]   

#     # Fetch all documents with optional category filter
#     if category:
#         filtered_books = list(collection.find({"category": category}))
#     else:
#         filtered_books = list(collection.find())

#     # Clean and prepare data

#     embeddings = []
#     valid_books = []

#     for book in filtered_books:
#         if 'embedding' in book:
#             embedding = np.array(book['embedding'])
#             if embedding.shape == query_embedding.shape:
#                 embeddings.append(embedding)
#                 book['_id'] = str(book['_id'])
#                 valid_books.append(book)

#     if not embeddings:
#         return jsonify([])

#     # Calculate cosine similarity
#     scores = cosine_similarity([query_embedding], embeddings)[0]  
#     top_indices = np.argsort(scores)[::-1][:10]

#     # Return top similar books
#     top_books = []
#     for i in top_indices:
#         book = valid_books[i]
#         book['similarity'] = float(scores[i])
#         top_books.append(book)

#     return jsonify(top_books)


# @app.route('/search/<query>/', defaults={'category': None}, methods=['POST'])
# @app.route('/search/<query>/<category>', methods=['POST'])
# def search(query, category):
#     data = request.get_json()
#     query = data.get("query", "")

#     Generate embedding for the query
#     query_embedding = model.encode(query, convert_to_tensor=True)

#     Compute cosine similarity
#     scores = util.cos_sim(query_embedding, book_embeddings)[0].cpu().numpy()
#     top_indices = np.argsort(scores)[::-1][:10]

#     Get the top books based on similarity
#     top_books = [books[i] for i in top_indices]

#     return jsonify(top_books)


if __name__  == "__main__":
    app.run(debug = True)