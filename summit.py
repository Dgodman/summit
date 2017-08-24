from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from string import punctuation
from collections import Counter
import re


RUN_TEST = False
EOS_CHARS = '.?!'
EXAMPLE_TITLE = "Barcelona searches for van driver who killed more than dozen along iconic promenade"
EXAMPLE_FILE = 'sample.txt'
STOPWORDS = set(stopwords.words('english'))
STOPWORDS_CUSTOM = \
    {"a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as",
     "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot",
     "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't",
     "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", 'has', "hasn't", "have", "haven't",
     "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his",
     "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its",
     "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on",
     "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't",
     "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the",
     "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll",
     "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't",
     "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where",
     "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you",
     "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves", "—", "’", "“", "”", "\"", "''",
     '``', }

STOPWORDS_CUSTOM_BIG = \
    {"a", "about", "above", "across", "after", "again", "against", "all", "almost", "alone", "along",
     "already", "also", "although", "always", "among", "an", "and", "another", "any", "anybody", "anyone", "anything",
     "anywhere", "are", "area", "areas", "around", "as", "ask", "asked", "asking", "asks", "at", "away", "b", "back",
     "backed", "backing", "backs", "be", "became", "because", "become", "becomes", "been", "before", "began", "behind",
     "being", "beings", "best", "better", "between", "big", "both", "but", "by", "c", "came", "can", "cannot", "case",
     "cases", "certain", "certainly", "clear", "clearly", "come", "could", "d", "did", "differ", "different",
     "differently", "do", "does", "done", "down", "down", "downed", "downing", "downs", "during", "e", "each", "early",
     "either", "end", "ended", "ending", "ends", "enough", "even", "evenly", "ever", "every", "everybody", "everyone",
     "everything", "everywhere", "f", "face", "faces", "fact", "facts", "far", "felt", "few", "find", "finds", "first",
     "for", "from", "full", "fully", "further", "furthered", "furthering", "furthers", "g", "gave", "general",
     "generally", "get", "gets", "give", "given", "gives", "go", "going", "good", "goods", "got", "great", "greater",
     "greatest", "group", "grouped", "grouping", "groups", "h", "had", "has", "have", "having", "he", "her", "here",
     "herself", "high", "higher", "highest", "him", "himself", "his", "how", "however", "i", "if", "important", "in",
     "interest", "interested", "interesting", "interests", "into", "is", "it", "its", "itself", "j", "just", "k",
     "keep", "keeps", "kind", "knew", "know", "known", "knows", "l", "large", "largely", "last", "later", "latest",
     "least", "less", "let", "lets", "like", "likely", "long", "longer", "longest", "m", "made", "make", "making",
     "man", "many", "may", "me", "member", "members", "men", "might", "more", "most", "mostly", "mr", "mrs", "much",
     "must", "my", "myself", "n", "necessary", "need", "needed", "needing", "needs", "never", "new", "new", "newer",
     "next", "no", "nobody", "non", "noone", "not", "nothing", "now", "nowhere", "number", "numbers", "o", "of", "off",
     "often", "old", "older", "oldest", "on", "once", "one", "only", "open", "opened", "opening", "opens", "or",
     "order", "ordered", "ordering", "orders", "other", "others", "our", "out", "over", "p", "part", "parted",
     "parting", "parts", "per", "perhaps", "place", "places", "point", "pointed", "pointing", "points", "possible",
     "present", "presented", "presenting", "presents", "problem", "problems", "put", "puts", "q", "quite", "r",
     "rather", "really", "right", "right", "room", "rooms", "s", "said", "same", "saw", "say", "says", "second",
     "seconds", "see", "seem", "seemed", "seeming", "seems", "sees", "several", "shall", "she", "should", "show",
     "showed", "showing", "shows", "side", "sides", "since", "small", "smaller", "smallest", "so", "some", "somebody",
     "someone", "something", "somewhere", "state", "states", "still", "such", "sure", "t", "take", "taken", "than",
     "that", "the", "their", "them", "then", "there", "therefore", "these", "they", "thing", "things", "think",
     "thinks", "this", "those", "though", "thought", "thoughts", "through", "thus", "to", "today", "together", "too",
     "took", "toward", "turn", "turned", "turning", "turns", "u", "under", "until", "up", "upon", "us", "use", "used",
     "uses", "v", "very", "w", "want", "wanted", "wanting", "wants", "was", "way", "ways", "we", "well", "wells",
     "went", "were", "what", "when", "where", "whether", "which", "while", "who", "whole", "whose", "why", "will",
     "with", "within", "without", "work", "worked", "working", "works", "would", "x", "y", "year", "years", "yet",
     "you", "young", "younger", "youngest", "your", "yours", "z", "—", "’", "“", "”", "\"", "''", '``', }


clean_regexps = [
    # uniform quotes
    (re.compile(r'\'\''), r'"'),
    (re.compile(r'``'), r'"'),
    (re.compile(r'“'), r'"'),
    (re.compile(r'”'), r'"'),
    # move punctuation outside quotes
    (re.compile(r'([\w])([.!?])(\")'), r'\1\3\2'),
]


# clean up text with regexpr
def clean_text(text):
    if text:
        for (regexp, repl) in clean_regexps:
            text = regexp.sub(repl, text)
    return text


# combine neighbor sentences with one quote each
def combine_quotes(sent_tokens):
    sentences = []
    index = 0
    while index < len(sent_tokens)-1:
        s1 = sent_tokens[index]
        s2 = sent_tokens[index+1]
        if s1.count('"') == 1 and s2.count('"') == 1:
            s1 += " " + s2
            index += 2
        else:
            index += 1
        sentences.append(s1)
    return sentences


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
if RUN_TEST and EXAMPLE_TEXT:
    print(len(EXAMPLE_TEXT))
    # tokenize text
    print("WORD TOKENS")
    word_tokens = split_words(EXAMPLE_TEXT)
    print(word_tokens)
    word_frequency = Counter(word_tokens)
    print(word_frequency)
    # filter stopwords
    stop_words = set(stopwords.words('english'))
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
    # stemmer = SnowballStemmer("english")
    # lemmer = WordNetLemmatizer()
    # lemmed_words = []

    for w in filtered_words:
        # .append(lemmer.lemmatize(w))
        stemmed_words.append(stemmer.stem(w))
    # get frequency
    word_frequency = Counter(stemmed_words)
    print("FILTERED & STEMMED WORD TOKENS")
    print(stemmed_words)
    print(word_frequency)
    # word_frequency = Counter(lemmed_words)
    # print(lemmed_words)
    # print(word_frequency)


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
        self.stemmer = None
        self.lemmatizer = None
        self.generate(text)

    def generate(self, text):
        # content
        self.text = clean_text(text)
        # stop words
        self.stop_words = STOPWORDS_CUSTOM_BIG
        self.words_cleaned = []
        # paragraphs
        print("Parsing paragraphs...")
        self.paragraphs = split_paragraphs(self.text)
        # sentences
        print("Parsing sentences...")
        self.sentences = combine_quotes(split_sentences(self.text))
        print("Parsing words...")
        self.words = split_words(self.text)
        print("Done.")

    # set stemmer type
    def set_stemmer(self, stem_type):
        if not stem_type:
            self.stemmer = None
        else:
            stem_type = stem_type.lower()
        if stem_type == "porter":
            self.stemmer = PorterStemmer()
        elif stem_type == "snowball":
            self.stemmer = SnowballStemmer("english")

    def set_lemmatizer(self, lem_type="default"):
        self.stemmer = None
        if not lem_type:
            self.lemmatizer = None
        else:
            self.lemmatizer = WordNetLemmatizer()

    # do stemming
    def stem_words(self, text):
        stemmed = []
        if self.stemmer:
            for word in self.clean_words(text):
                stemmed.append(self.stemmer.stem(word))
        return stemmed

    # do lemming
    def lem_words(self, text):
        lemmed = []
        if self.lemmatizer:
            for word in self.clean_words(text):
                lemmed.append(self.lemmatizer.lemmatize(word))
        return lemmed

    # 2d array that compares likenesses of sentences
    def sent_intersections(self, clean=False):
        intersects = []
        n = len(self.sentences)
        if n > 0:
            # zeroed 2d array
            intersects = [[0] * n for _ in range(n)]
            for i in range(0, n):
                s1 = self.sentences[i]
                if clean:
                    s1 = self.clean_words(s1)
                else:
                    s1 = split_words(s1)
                s1 = set(s1)
                for j in range(0, n):
                    s2 = self.sentences[j]
                    if clean:
                        s2 = self.clean_words(s2)
                    else:
                        s2 = split_words(s2)
                    s2 = set(s2)
                    intersects[i][j] = len(s1.intersection(s2)) / ((len(s1) + len(s2)) / 2)
        return intersects

    # remove stop words
    def clean_words(self, text):
        cleaned = []
        words = split_words(text)
        for word in words:
            word = word.lower()
            if word not in self.stop_words:
                if self.stemmer:
                    word = self.stemmer.stem(word)
                elif self.lemmatizer:
                    word = self.lemmatizer.lemmatize(word)
                cleaned.append(word)
        return cleaned

    # return words and their frequency
    def word_frequency(self, text):
        word_freq = []
        text_cleaned = self.clean_words(text)
        if text_cleaned:
            # word frequency
            wf = Counter(text_cleaned)
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
