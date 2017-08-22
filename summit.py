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


# tokenize by paragraphs
def split_paragraphs(text):
    tokens = []
    if text:
        # replace with single newlines
        temp_text = re.sub(r'\n+', '\n', text).strip()
        tokens = temp_text.split('\n')
    return tokens


# tokenize by sentences
def split_sentences(text):
    tokens = []
    if text:
        temp_text = re.sub(r'\n+', ' ', text).strip()
        tokens = sent_tokenize(temp_text)
    return tokens


# tokenize by words
def split_words(text):
    tokens = []
    if text:
        tokens = word_tokenize(text)
        tokens = [i for i in tokens if i not in punctuation]
    return tokens


def max_intersects(intersect):
    indices = []
    if len(intersect) > 0:
        indices = list(range(len(intersect)))
        indices.sort(reverse=True, key=lambda x: intersect[x])
    return indices


EXAMPLE_TEXT = read_file()
if not PYTHON_SHELL and EXAMPLE_TEXT:
    print(len(EXAMPLE_TEXT))
    # tokenize text
    print("WORD TOKENS")
    word_tokens = split_words(EXAMPLE_TEXT)
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


class Summarize:
    """
    Represents concepts built from common key words from text
    """
    def __init__(self, text):
        self.text = None
        self.stop_words = None
        self.words_cleaned = None
        self.paragraphs = None
        self.sentences = None
        self.words = None
        self.generate(text)

    def generate(self, text):
        # content
        self.text = text
        # stop words
        self.stop_words = STOP_WORDS
        self.stop_words.update(EXTRA_STOP_WORDS)
        self.words_cleaned = []
        # paragraphs
        print("Parsing paragraphs...")
        self.paragraphs = split_paragraphs(self.text)
        # sentences
        print("Parsing sentences...")
        self.sentences = split_sentences(self.text)
        print("Parsing words...")
        self.words = split_words(self.text)
        print("Done.")

    def get_sentence_intersects(self, clean=False):
        intersects = []
        n = len(self.sentences)
        if n > 0:
            # zeroed 2d array
            intersects = [[0] * n for _ in range(n)]
            for i in range(0, n):
                s1 = split_words(self.sentences[i])
                if clean:
                    s1 = self.clean(s1)
                s1 = set(s1)
                for j in range(0, n):
                    s2 = split_words(self.sentences[j])
                    if clean:
                        s2 = self.clean(s2)
                    s2 = set(s2)
                    intersects[i][j] = len(s1.intersection(s2)) / ((len(s1) + len(s2)) / 2)
        return intersects

    def clean(self, text):
        cleaned = []
        words = self.split_words(text)
        for word in words:
            word = word.lower()
            if word not in self.stop_words:
                cleaned.append(word)
        return cleaned

    def word_frequency(self, text):
        word_freq = []
        clean_text = self.clean(text)
        if clean_text:
            # word frequency
            wf = Counter(clean_text)
            # sorted list
            word_freq = wf.most_common()
        return word_freq


class Sentence:
    """
    Represents a sentence object
    """
    def __init__(self, text):
        # set sentence text
        self.text = text
        # split words
        self.words = split_words(self.text)
