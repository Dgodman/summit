from utils import *
from math import log
from collections import defaultdict
from operator import itemgetter
from nltk.stem import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from collections import Counter
from nltk.tokenize import sent_tokenize, word_tokenize
from string import punctuation


PORTER = PorterStemmer()
SNOWBALL = SnowballStemmer('english')
WORDNET = WordNetLemmatizer()


class AbstractTokenizer:
    def __init__(self, _stemmer=None, _stopwords=STOPWORDS_CUSTOM):
        self.text = ""
        self.paragraphs = []
        self.sentences = []
        self.words = []
        self.sentence_words = []
        self.stop_words = _stopwords
        self.stemmer = _stemmer

    def __call__(self, _stemmer=None, _stopwords=None):
        if _stemmer or _stopwords:
            self.sentence_words = []
            self.words = []
            if _stemmer:
                self.stemmer = _stemmer
            if _stopwords:
                self.stop_words = _stopwords

    # combine sentences surrounded by quotes
    @staticmethod
    def combine_quotes(sent_list):
        combined_sentences = []
        i = 0
        length = len(sent_list)
        while i < length:
            s1 = sent_list[i]
            if s1.count('"') == 1:
                j = i + 1
                while i != j and j < length:
                    s2 = sent_list[j]
                    if s2.count('"') == 1:
                        s1 += s2
                        i = j
                    else:
                        j += 1
            i += 1
            combined_sentences.append(s1)
        return combined_sentences

    # tokenize by paragraphs
    @staticmethod
    def split_paragraphs(text):
        tokens = []
        if text:
            # replace with single newlines
            temp_text = re.sub(r'\n+', '\n', text).strip()
            tokens = temp_text.split('\n')
        return tokens

    # tokenize by sentences
    @classmethod
    def split_sentences(cls, text):
        tokens = []
        if text:
            temp_text = re.sub(r'\n+', ' ', text).strip()
            tokens = sent_tokenize(temp_text)
        return cls.combine_quotes(tokens)

    # tokenize by words
    @staticmethod
    def split_words(text):
        tokens = []
        if text:
            tokens = word_tokenize(text)
            tokens = [i.lower() for i in tokens if i not in punctuation]
        return tokens

    # clean up text with regexpr
    @staticmethod
    def prep_doc(text):
        if text:
            text = text.replace('\u200b', '')
            for (regexp, repl) in clean_regexps:
                text = regexp.sub(repl, text)
        return text

    def tokenize(self, _text, token_p=True, token_s=True, token_w=True):
        self.reset_vars()
        self.text = self.prep_doc(_text)
        # paragraphs
        if token_p:
            self.paragraphs = self.split_paragraphs(self.text)
        if token_s:
            # sentences
            self.sentences = self.split_sentences(self.text)
        if token_w:
            for sent in self.sentences:
                words = self.clean_words(sent)
                self.sentence_words.append(words)
                self.words.extend(words)

    def reset_vars(self):
        self.text = ""
        self.paragraphs = []
        self.sentences = []
        self.words = []
        self.sentence_words = []

    def stem(self, _word):
        if self.stemmer and _word:
            _word = STEM_DICT.get(_word, _word)
            if isinstance(self.stemmer, WordNetLemmatizer):
                noun = self.stemmer.lemmatize(_word, 'n')
                verb = self.stemmer.lemmatize(_word, 'v')
                if verb != _word:
                    return verb
                else:
                    return self.finagle(noun)
            else:
                return self.stemmer.stem(_word)
        return _word

    # split text into words + filter words + stem words
    def clean_words(self, _text):
        return self.stem_words(self.filter_stop_words(self.split_words(_text)))

    # remove stop words from list
    def filter_stop_words(self, _word_list):
        filtered = []
        if _word_list and self.stop_words:
            # remove stop words
            for word in _word_list:
                if word not in self.stop_words:
                    filtered.append(word)
            return filtered
        else:
            return _word_list

    @staticmethod
    def finagle(_word):
        noun_subs = [('ches', 'ch'), ('shes', 'sh'), ('ves', 'f'), ('ses', 's'), ('xes', 'x'), ('zes', 'z'),
                     ('men', 'man'), ('ies', 'y'), ('ss', 'ss'), ('s', '')]
        for end_sub in noun_subs:
            old = end_sub[0]
            new = end_sub[1]
            if _word[-len(old):] == old:
                return _word[:-len(old)] + new
        return _word

    def stem_words(self, _word_list):
        stemmed = []
        if _word_list and self.stemmer:
            for word in _word_list:
                stemmed.append(self.stem(word))
            return stemmed
        else:
            return _word_list

    def wf(self, _as_percent=False):
        word_dict = {}
        if self.words:
            word_len = len(self.words)
            c = Counter(self.words).most_common()
            for wc in c:
                s = wc[0]
                i = wc[1]
                if _as_percent:
                    i = i / word_len
                word_dict[s] = i
        return word_dict

    def key_words(self):
        return list(self.wf())

    def get_sentence_words(self, i):
        words = self.sentence_words[i]
        if not words:
            words = self.clean_words(self.sentences[i])
        return words

    def get_phrases(self, _phrase_length=2):
        phrase_dict = defaultdict(float)
        # loop sentences
        for sent in self.sentences:
            # get word list from sentence
            word_list = self.clean_words(sent)
            # get length of list
            n = len(word_list)
            # create dict[word[n] word[n+1]]
            for i in range(0, n):
                max_j = min(i + _phrase_length, n)
                phrase = word_list[i]
                for j in range(i + 1, max_j):
                    phrase += " " + word_list[j]
                    phrase_dict[phrase] += 1
        # remove items with 1 or less
        phrases = {}
        for k, v in phrase_dict.items():
            if v > 1:
                phrases[k] = v
        if phrases:
            phrases = sorted(phrases.items(), key=itemgetter(1), reverse=True)
        return phrases


class Summus(AbstractTokenizer):
    def __init__(self, _text=None, _stemmer=WORDNET):
        super(Summus, self).__init__(_stemmer)
        if _text:
            self.tokenize(_text)

    def __call__(self, _text=None):
        if _text:
            self.tokenize(_text)

    def tokenize(self, _text, token_p=True, token_s=True, token_w=True):
        super(Summus, self).tokenize(_text, token_p, token_s, token_w)

    @staticmethod
    def rank_edges(_words1, _words2):
        rank = 0.0
        norm = 0.0
        for w1 in _words1:
            for w2 in _words2:
                rank += int(w1 == w2)
        if len(_words1) > 0 and len(_words2) > 0:
            norm = log(len(_words1)) + log(len(_words2))
        if norm == 0.0:
            return 0.0
        else:
            return rank / norm

    def score_sentences(self):
        sentence_ranks = []
        n = len(self.sentences)
        if n > 0:
            # 2d array with zeros
            sentence_matrix = [[0.0] * n for _ in range(n)]
            # rows
            for i in range(0, n):
                s1 = self.get_sentence_words(i)
                s1 = set(s1)
                # columns
                for j in range(0, n):
                    rank = 0.0
                    if len(s1) > 0 and i != j:
                        s2 = self.get_sentence_words(j)
                        s2 = set(s2)
                        rank = self.rank_edges(s1, s2)
                    sentence_matrix[i][j] = rank
            for i in range(0, n):
                rank = 0.0
                for j in range(0, n):
                    rank += sentence_matrix[i][j]
                sentence_ranks.append(rank)
        return sentence_ranks

    def get_ranked_sentences(self, _percent=.6, _count=-1):
        if not _percent or _percent <= 0 or _percent > 1:
            _percent = 0.6
        if not _count or _count <= 0:
            _count = int(round(len(self.sentences) * (1 - _percent)))
        ranked_indexes = sorted(self.rank_sentences()[:_count])
        rank_text = ""
        if len(ranked_indexes) > 0:
            for i in ranked_indexes:
                rank_text += self.sentences[i] + " "
        return rank_text

    def rank_sentences(self):
        scores = self.score_sentences()
        return sort_by_index(scores)

    def print_ranked_paragraphs(self, _count=-1):
        if not _count or _count <= 0:
            _count = int(len(self.sentences) * 0.20)
        ranked_indexes = sorted(self.rank_paragraphs()[:_count])
        if len(ranked_indexes) > 0:
            rank_text = ""
            for i in ranked_indexes:
                rank_text += self.paragraphs[i] + "\n"
            print(rank_text)
        else:
            print("No paragraphs to print.")

    def rank_paragraphs(self):
        inters = []
        key_list = []
        # get length
        n = len(self.paragraphs)
        # create list of keywords for each paragraph
        for p in self.paragraphs:
            key_list.append(self.key_words(p))
        # compare each paragraph with another
        for i in range(0, n):
            interval = 0
            k1 = set(key_list[i])
            k2 = set()
            for j in range(0, n):
                if i != j:
                    k2 = set(key_list[j])
                    interval += len(k1.intersection(k2))
            norm = log(len(k1)) + log(len(k2))
            if norm == 0.0:
                interval = 0.0
            else:
                interval = interval / norm
            inters.append(interval)
        return sort_by_index(inters)
