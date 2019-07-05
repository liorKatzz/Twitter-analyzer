from datetime import datetime
import string
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer

DAY_OF_WEEK = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
WORDS_TO_EXCLUDE = {'http', 'https', 'co', 'rt', 'realdonaldtrump', 'trump', 'u', 'many'}


def str_to_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return -1


def remove_belonging(text: str):
    """
    Removing the 's from names
    """
    text = text.replace('’s', '')
    return text


def remove_punctuation(s: str):
    return s.translate(str.maketrans('', '', string.punctuation))


def my_tokenizer(text: str):
    """ Return tokens, remove punctuations as well"""
    tokenizer = RegexpTokenizer(r'\w+')
    return tokenizer.tokenize(text)


def remove_stopwords_from_tokens(tokens):
    stopwords_set = set(stopwords.words('english'))

    def add_to_stopwords(words):
        for word in words:
            stopwords_set.add(word)

    add_to_stopwords(WORDS_TO_EXCLUDE)
    return [w for w in tokens if w not in stopwords_set]


def remove_stopwords_from_str(s: str):
    stopwords_set = set(stopwords.words('english'))

    def add_to_stopwords(excluded_words):
        for ex_word in excluded_words:
            stopwords_set.add(ex_word)

    add_to_stopwords(WORDS_TO_EXCLUDE)
    words = s.split()
    return ' '.join([word for word in words if word not in stopwords_set])


def to_lower(tokens):
    return [w.lower() for w in tokens]


def lemmatize(tokens):
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(w) for w in tokens]


def parse_text(text: str):
    # Fetching the text
    tokens = my_tokenizer(text)
    # To lowercase
    tokens = to_lower(tokens)
    # Removing stop words
    tokens = remove_stopwords_from_tokens(tokens)
    # Lemmatizing
    tokens = lemmatize(tokens)
    return tokens



