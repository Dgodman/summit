from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from string import punctuation
from collections import Counter
import re


EXAMPLE_TITLE = "Barcelona searches for van driver who killed more than dozen along iconic promenade"
EXAMPLE_FILE = 'sample.txt'
EXTRA_STOP_WORDS = {'—', '’', '“', '”', }
PYTHON_SHELL = True
STOP_WORDS = set(stopwords.words('english'))
STOP_WORDS.update(EXTRA_STOP_WORDS)


# read text from a file
def read_file(filename=""):
    if not filename:
        filename = EXAMPLE_FILE
    with open(filename, encoding="utf8") as f:
        text = f.read()
        text = text.replace(u'\ufeff', '')
    if text:
        text = text.strip()
    return text


# tokenize words and remove punctuation
def word_tokens(text):
    tokens = word_tokenize(text)
    tokens = [i for i in tokens if i not in punctuation]
    return tokens


# tokenize sentences
def sent_tokens(text):
    tokens = sent_tokenize(text)
    return tokens


EXAMPLE_TEXT = read_file()
if not PYTHON_SHELL and EXAMPLE_TEXT:
    print(len(EXAMPLE_TEXT))
    # tokenize text
    print("WORD TOKENS")
    word_tokens = word_tokens(EXAMPLE_TEXT)
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


class Concepts:
    """
    Represents concepts built from common key words from text
    """
    def __init__(self, text):
        # content
        self.text = text
        # stop words
        self.stop_words = STOP_WORDS
        self.stop_words.update(EXTRA_STOP_WORDS)
        self.words_filtered = []
        # paragraphs
        print("Parsing paragraphs...")
        self.paragraphs = self.split_paragraphs()
        # sentences
        print("Parsing sentences...")
        self.sentences = self.split_sentences()
        print("Parsing words...")
        self.words = self.split_words()
        for word in self.words:
            word = word.lower()
            if word not in self.stop_words:
                self.words_filtered.append(word)

    def split_paragraphs(self):
        tokens = []
        if self.text:
            # replace with single newlines
            temp_text = re.sub(r'\n+', '\n', self.text).strip()
            tokens = temp_text.split('\n')
        return tokens

    def split_sentences(self):
        tokens = []
        if self.text:
            tokens = sent_tokenize(self.text)
        return tokens

    def split_words(self):
        tokens = []
        if self.text:
            tokens = word_tokenize(self.text)
            tokens = [i for i in tokens if i not in punctuation]
        return tokens


class Sentence:
    """
    Represents a sentence object
    """
    def __init__(self, text, filter_words=True):
        # set sentence text
        self.text = text
        # split words
        self.words = []
        if self.text:
            self.words = word_tokenize(self.text)
            # filter words
            if filter_words:
                words_filtered = []
                for word in self.words:
                    word = word.lower()
                    if word not in STOP_WORDS:
                        words_filtered.append(word)
                self.words = filtered_words
            # set word count
            self.word_count = len(self.words)

    def get_words(self):
        return self.words
