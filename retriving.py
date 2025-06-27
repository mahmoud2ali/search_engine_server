import pickle
from sentence_transformers import SentenceTransformer
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from preprocessing import preprocess_text
from collections import Counter
from sentence_transformers import util

# Load the inverted index from the file
with open('inverted_index.pkl', 'rb') as f:
    inverted_index = pickle.load(f)

with open('inverted_index_dict_within_5_length_query.pkl', 'rb') as f:
    inverted_index_dict_within_5_length_query = pickle.load(f)

print("Inverted index loaded successfully.")

# print(loaded_inverted_index.get("specific_word"))

# Load embedding dictionary
with open('embedding_dict.pkl', 'rb') as f:
    embedding_dict = pickle.load(f)

print("Embedding dictionary loaded successfully.")

model = SentenceTransformer('./model')

# import preprocessed data  
df = pd.read_csv('./dataset/preprocessed_data.csv')
df_original = pd.read_excel('./dataset/books_data.xlsx')

# searching 
# update
def most_repeated(numbers):
    counter = Counter(numbers)
    return counter.most_common()






def get_embeddings_and_apply_cosine_similarity(row_ids, query, query_genre, threshold=0.85):
    query = preprocess_text(query)
    query_embedding = model.encode([query])[0]  # get embedding as 1D array
    similarities_final_retrieved_ids = []

    for idx in row_ids:
        book_genre = df.loc[idx, "Genres"]  # Or whatever your genre column is
        if book_genre == query_genre:
            # print("here")
            book_embedding = embedding_dict[idx] # Convert tensor to numpy for cosine_similarity
            similarity = cosine_similarity(query_embedding.reshape(1, -1), book_embedding.reshape(1, -1))[0][0]
            # print(similarity)
            # Append to results only if similarity meets the threshold
            if similarity >= threshold:
                # print("here")
                similarities_final_retrieved_ids.append((similarity, idx))

    # Sort by similarity descending
    similarities_final_retrieved_ids.sort(key=lambda x: x[0], reverse=True)
    return similarities_final_retrieved_ids



def search(query_str, query_genre=None, threshold=0.85):
    words = query_str.split()
    matched_rows = set()
    rows = []

    if len(words) <= 10:
        for word in words:
            if word in inverted_index_dict_within_5_length_query:
                rows += inverted_index_dict_within_5_length_query[word]

        row_ids = most_repeated(rows)

        results = []
        if len(row_ids) > 0:

            for row_id, count in row_ids:
                book_id = df.loc[row_id, "id"]  # Get book ID from preprocessed df
                book_info = df_original.loc[df_original["id"] == book_id].iloc[0].to_dict()

                results.append(book_info)
            return results
        else:
            return []

    else:
        for word in words:
            if word in inverted_index:
                matched_rows.update(inverted_index[word])

        rows.extend(matched_rows)
        # print(rows)
        results = get_embeddings_and_apply_cosine_similarity(rows, query_str, query_genre, threshold)
        # print(results)
        if results:
            output = []
            for sim, idx in results:
                    book_id = df.loc[idx, "id"]
                    # Get metadata from original_df using BookID
                    book_info = df_original.loc[df_original["id"] == book_id].iloc[0]
                    book_info = book_info.to_dict()
                    output.append(book_info)
            return output  

        else:
            print("⚠️ لم يتم العثور على نتائج متشابهة ")


