import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def download_nltk_data():
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)
    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        nltk.download('wordnet', quiet=True)
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)

download_nltk_data()

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
KEEP_WORDS = {'not', 'no', 'nor'}
stop_words -= KEEP_WORDS

def clean_text(text):
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'\S+@\S+', ' ', text)
    text = re.sub(r'http\S+|www\S+', ' ', text)
    text = re.sub(r'[^a-z\s\+\#]', ' ', text)
    text = text.replace('c++', 'cplusplus')
    text = text.replace('c#', 'csharp')
    text = text.replace('.net', 'dotnet')
    text = re.sub(r'\s+', ' ', text).strip()
    tokens = text.split()
    cleaned_tokens = []
    for token in tokens:
        if token not in stop_words and len(token) > 1:
            lemma = lemmatizer.lemmatize(token)
            cleaned_tokens.append(lemma)
    return ' '.join(cleaned_tokens)

def preprocess_for_display(text):
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    return text