from flask import Flask, request, render_template
import pandas as pd 
import firebase_admin
from firebase_admin import credentials, firestore
from pymongo import MongoClient

app = Flask(__name__)


df = pd.read_csv("books_data.csv")


# Step 2: Connect to MongoDB (assumes it's running on localhost)
client = MongoClient("mongodb://localhost:27017/")
# client = MongoClient("mongodb+srv://admin-mahmoud:0123456789@cluster0.8w33a.mongodb.net/")


# Step 3: Create or connect to a database and collection
db = client['book_search_engine']
collection = db['books']

# Step 4: Insert data into the collection
collection.delete_many({})  # Optional: clear old data
collection.insert_many(df.to_dict(orient='records'))

print("Books inserted successfully into MongoDB!")


@app.route('/')
def index():
    return "hello, world!"


if __name__  == "__main__":
    app.run(debug = True)