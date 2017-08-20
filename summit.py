from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from string import punctuation
from collections import Counter


EXAMPLE_TITLE = "Barcelona searches for van driver who killed more than dozen along iconic promenade"
EXAMPLE_FILE = 'sample.txt'
EXTRA_STOP_WORDS = {'—', '’', '“', '”', }


# read text from a file
def read_file(filename=""):
    if not filename:
        filename = EXAMPLE_FILE
    with open(filename, encoding="utf8") as f:
        text = f.read()
    if text:
        text = text.strip()
    return text


# tokenize words and remove punctuation
def tokenize(text):
    tokens = word_tokenize(text)
    tokens = [i for i in tokens if i not in punctuation]
    return tokens


EXAMPLE_TEXT = read_file()
if EXAMPLE_TEXT:
    print(len(EXAMPLE_TEXT))
    # tokenize text
    print("WORD TOKENS")
    word_tokens = tokenize(EXAMPLE_TEXT)
    print(word_tokens)
    word_frequency = Counter(word_tokens)
    print(word_frequency)
    # filter stopwords
    stop_words = set(stopwords.words('english'))
    stop_words.update(EXTRA_STOP_WORDS)
    filtered_words = []
    for w in word_tokens:
        w = w.lower()
        if w not in stop_words:
            filtered_words.append(w)
    # print filtered list
    print("FILTERED WORD TOKENS")
    print(filtered_words)
    word_frequency = Counter(filtered_words)
    print(word_frequency)
    # stem word list
    stemmed_words = []
    stemmer = PorterStemmer()
    #stemmer = SnowballStemmer("english")
    #lemmer = WordNetLemmatizer()
    #lemmed_words = []

    for w in filtered_words:
        #.append(lemmer.lemmatize(w))
        stemmed_words.append(stemmer.stem(w))
    # get frequency
    word_frequency = Counter(stemmed_words)
    print("FILTERED & STEMMED WORD TOKENS")
    print(stemmed_words)
    print(word_frequency)
    #word_frequency = Counter(lemmed_words)
    #print(lemmed_words)
    #print(word_frequency)
