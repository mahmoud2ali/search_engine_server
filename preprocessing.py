import re
import string
import nltk
from nltk.corpus import stopwords
from snowballstemmer import stemmer

# One-time download (run once)
# nltk.download('stopwords')
arabic_stemmer = stemmer("arabic")

def stemming(text):
    return arabic_stemmer.stemWord(text)

# def remove_enter(text):
#   x = text.replace('\\n',' ')
#   return x

def remove_punctuation(text):
    arabic_punctuation = r"[،؛؟!٪ـ«»…\"\'٫٬٭\,.:؛؟!<>*”…“()\[\{}/\\_#$%&+;=?@^~`\]\|➖\u2014\u2013\u002D]"
    return re.sub(arabic_punctuation,' ', text)

def remove_repeated_whitespaces(text):
    return re.sub(r'(?<=\S)\s{2,}(?=\S)', ' ', text)

def remove_arabic_numbers(text):
    return re.sub(r'[\u0660-\u0669]', " ", text)

def remove_diacritics(text):
    arabic_diacritics = re.compile(r'[\u064B-\u065F]')
    return re.sub(arabic_diacritics, '', text)

def remove_all_except_arabic(text):
    return re.sub(r'[^\u0600-\u06FF\s]', ' ', text)

def remove_links(text):
  return re.sub(r'http[s]?://\S+|www\.\S+',' ',text)

def remove_stop_words(text):
    stop_words = set(stopwords.words('arabic'))  # Corrected function call
    words = text.split()  # Tokenize the text by spaces
    filtered_text = "  ".join([word for word in words if word not in stop_words])
    return filtered_text

def normalize_arabic(text):
    # Define normalization mapping
    normalization_map = {
        "إ": "ا",
        "أ": "ا",
        "آ": "ا",
        "ا": "ا",
        "ى": "ي",
        "ي": "ي",
        "ؤ": "و",
        "ئ": "ي",
        "ة": "ه",
        "گ": "ك",
        "ڤ": "ف",
        "چ": "ج",
        "پ": "ب",
    }

def remove_extra_newlines(text):
    return re.sub(r'\n+', ' ', text).strip()

    # Apply replacements using regex
    text = re.sub("|".join(map(re.escape, normalization_map.keys())),
                  lambda m: normalization_map[m.group()], text)

    return text



def preprocess_text(text):
    text = remove_diacritics(text)
    text = remove_links(text)
    text = remove_punctuation(text)
    text = remove_arabic_numbers(text)
    text = remove_all_except_arabic(text)
    # text = normalize_arabic(text)
    text = remove_stop_words(text)
    # text = remove_enter(text)
    text = remove_repeated_whitespaces(text)
    text = stemming(text)
    return text