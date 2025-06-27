import pandas as pd

# Read excel file
df = pd.read_excel('./data/books_data.xlsx')

#get random 10 books from the dataset
def get_random_books():
    books = df.sample(n=10).to_dict(orient='records')
    return books