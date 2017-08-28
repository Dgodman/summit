from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from string import punctuation
from collections import Counter
import re


"""
ISSUES:

- Key word scores can really skew sentence ranks. 
Example:    
Sentence 64 in Harvey article.
'They are fresh and hot, and I am selling a lot of them because people are stocking up for the hurricane.'
Has a score of 3.6665 despite it not really being "important". It contains the word 'hurricane' which is worth 
14 points. The rest of the sentence is meaningless, but because it has the 2nd highest word value then it 
 skews the whole sentence value.
"""


RUN_TEST = False
LEM_WORDS = False
STEMMER = PorterStemmer()
LEMMER = WordNetLemmatizer()
EOS_CHARS = '.?!'
EXAMPLE_TITLE = "Barcelona searches for van driver who killed more than dozen along iconic promenade"
HARVEY_TITLE = "Hurricane Harvey hits Texas, bringing heavy rain, storm surge"
EXAMPLE_FILE = 'sample.txt'
HARVEY_FILE = 'harvey.txt'
STOPWORDS_SMALL = set(stopwords.words('english'))
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
    {"a", "about", "above", "across", "after", "again", "against", "all", "almost", "alone", "along", "am",
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
     "order", "ordered", "ordering", "orders", "other", "others", "our", "out", "over", "p", "part", "parted", "people",
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
     "you", "young", "younger", "youngest", "your", "yours", "z", "-", "—", "’", "“", "”", "\"", "''", '``', }

STOPWORDS = STOPWORDS_CUSTOM_BIG

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
def prep_doc(text):
    if text:
        for (regexp, repl) in clean_regexps:
            text = regexp.sub(repl, text)
    return text


# remove stop words from entire text
def trim_text(text, _stem=False):
    return trim_words(split_words(text), _stem)


# remove stop words from list
def trim_words(words, _stem=False):
    trimmed = []
    # remove stop words
    for word in words:
        if word not in STOPWORDS:
            trimmed.append(word)
    # stem after
    if _stem:
        trimmed = stem_words(trimmed)
    return trimmed


# stem entire text
def stem_text(text):
    words_stemmed = []
    for word in split_words(text):
        words_stemmed.append(STEMMER.stem(word))
    return words_stemmed


# stem list of words
def stem_words(words):
    words_stemmed = []
    for word in words:
        words_stemmed.append(STEMMER.stem(word))
    return words_stemmed


# combine neighbor sentences with one quote each
def combine_quotes(sent_tokens):
    sentences = []
    index = 0
    while index < len(sent_tokens):
        s1 = sent_tokens[index]
        if index+1 < len(sent_tokens):
            s2 = sent_tokens[index+1]
        else:
            s2 = ""
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
        filename = HARVEY_FILE
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
        tokens = [i.lower() for i in tokens if i not in punctuation]
    return tokens


# sort a list and return its sorted indexes
def sort_by_index(list_to_sort):
    indices = []
    if len(list_to_sort) > 0:
        indices = list(range(len(list_to_sort)))
        indices.sort(reverse=True, key=lambda x: list_to_sort[x])
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


class AbstractTokenizer:
    def __init__(self, _text):
        self.text = prep_doc(_text)
        self.doc = []
        self.words = []
        self.paragraphs = []
        self.sentences = []
        self.words_trimmed = []
        self.words_stemmed = []
        self.stop_words = STOPWORDS_CUSTOM_BIG
        self.do_trim = False
        self.do_stem = False
        self.do_normalize = False
        # self.tokenize()

    def tokenize(self, token_p=True, token_s=True, token_w=True):
        # paragraphs
        if token_p:
            self.paragraphs = split_paragraphs(self.text)
        if token_s:
            # sentences
            self.sentences = combine_quotes(split_sentences(self.text))
        if token_w:
            self.words = split_words(self.text)
            self.words_trimmed = trim_words(self.words)
            self.words_stemmed = stem_words(self.words_trimmed)

    def setup(self, _trim=False, _stem=False, _normalize=False):
        self.do_trim = _trim
        self.do_stem = _stem
        self.do_normalize = _normalize

    def word_count(self, _text=None):
        word_count = {}
        if _text:
            words = split_words(_text)
            if self.do_trim:
                words = trim_words(words)
            elif self.do_stem:
                words = stem_words(trim_words(words))
        else:
            words = self.words
            if self.do_trim:
                words = self.words_trimmed
            if self.do_stem:
                words = self.words_stemmed
        if words:
            c = Counter(words).most_common()
            for wc in c:
                s = wc[0]
                i = wc[1]
                word_count[s] = i
        return word_count

    def key_words(self, _count=-1, _text=None):
        key_words = list(self.word_count(_text))
        if len(key_words) > 0:
            if not _count or _count <= 0:
                _count = len(key_words)
            key_words = key_words[:_count]
        return key_words


class Paragraph(AbstractTokenizer):
    def __init__(self, _text):
        super(Paragraph, self).__init__(_text)
        self.tokenize(token_p=False)


class Sentence(AbstractTokenizer):
    def __init__(self, _text):
        super(Sentence, self).__init__(_text)
        self.tokenize(token_p=False, token_s=False)


class Ranker(AbstractTokenizer):
    def __init__(self, _text):
        super(Ranker, self).__init__(_text)
        self.setup(_trim=True, _stem=True, _normalize=True)
        self.tokenize()

    def print_top_sentences(self, _count=-1):
        for i in sorted(self.top_sentences(_count)):
            print(self.sentences[i], " ")

    def top_sentences(self, _count=-1):
        # 25% if no count given
        if not _count or _count <= 0:
            _count = int(len(self.sentences) * 0.25)
        # 100% if count >
        if _count > len(self.sentences):
            _count = len(self.sentences)
        # score all sentences
        sent_scores = self.rank_sentences()
        # sort by index
        sorted_indexes = sort_by_index(sent_scores)[:_count]
        # return sentences
        return sorted_indexes

    def rank_sentences(self):
        scores = []
        # score all sentences
        for sent in self.sentences:
            scores.append(self.score_sentence(sent))
        return scores

    def score_sentence(self, _sentence):
        # stem sentence
        sent = trim_text(_sentence, True)
        # get word ranks
        word_scores = self.word_count()
        # sum words in sentence
        score = 0
        for word in sent:
            score += word_scores.get(word, 0)
        if score > 0:
            score = score / len(sent)
        return score


class Summarize:
    """
    Summarize text from key words
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
        self.text = prep_doc(text)
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
                cleaned.append(word)
        return cleaned

    def key_words(self, text, num=-1):
        key_words = {}
        wf = self.word_frequency(text)
        if wf:
            if not num or num <= 0:
                num = len(wf)
            for w in wf[:num]:
                key_words[w[0]] = w[1]
        return key_words

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
