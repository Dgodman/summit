from utils import *
from math import log


class AbstractTokenizer:
    def __init__(self, stem_lang=None):
        self.text = ""
        self.paragraphs = []
        self.sentences = []
        self.words = []
        self.stop_words = STOPWORDS_CUSTOM_BIG
        self.stemmer = None
        if stem_lang.lower() == "english":
            self.stemmer = SnowballStemmer("english")

    def tokenize(self, _text, token_p=True, token_s=True, token_w=True):
        self.text = prep_doc(_text)
        # paragraphs
        if token_p:
            self.paragraphs = split_paragraphs(self.text)
        if token_s:
            # sentences
            self.sentences = split_sentences(self.text)
        if token_w:
            self.words = self.clean_words(_text)

    # split text into words + filter words + stem words
    def clean_words(self, _text):
        return self.stem_words(self.filter_stop_words(split_words(_text)))

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

    # stem words
    def stem_words(self, _word_list):
        stemmed = []
        if _word_list and self.stemmer:
            for word in _word_list:
                stemmed.append(self.stemmer.stem(word))
            return stemmed
        else:
            return _word_list

    def word_frequency(self, _text=None):
        word_count = {}
        if not _text:
            _text = self.text
        words = self.clean_words(_text)
        if words:
            c = Counter(words).most_common()
            for wc in c:
                s = wc[0]
                i = wc[1]
                word_count[s] = i
        return word_count

    def key_words(self, _text=None):
        if not _text:
            _text = self.text
        return list(self.word_frequency(_text))


class Rankit(AbstractTokenizer):
    def __init__(self, stem_lang="english"):
        super(Rankit, self).__init__(stem_lang)
        self.sentence_words = []

    def tokenize(self, _text, token_p=True, token_s=True, token_w=True):
        super(Rankit, self).tokenize(_text, token_p, token_s, token_w)
        for sent in self.sentences:
            words = self.clean_words(sent)
            self.sentence_words.append(words)

    def get_sentence_words(self, i):
        words = self.sentence_words[i]
        if not words:
            words = self.clean_words(self.sentences[i])
        return words

    @staticmethod
    def rank_edges(_words1, _words2):
        rank = 0.0
        norm = 0.0
        for w1 in _words1:
            for w2 in _words2:
                rank += int(w1 == w2)
        if rank > 0 and len(_words1) > 0 and len(_words2) > 0:
            norm = log(len(_words1)) + log(len(_words2))
        if not norm or norm == 0.0:
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

    def print_ranked_sentences(self, _count=-1):
        if not _count or _count <= 0:
            _count = int(len(self.sentences) * 0.20)
        ranked_indexes = sorted(self.rank_sentences()[:_count])
        if len(ranked_indexes) > 0:
            rank_text = ""
            for i in ranked_indexes:
                rank_text += self.sentences[i] + " "
            print(rank_text)
        else:
            print("No sentences to print.")

    def rank_sentences(self):
        scores = self.score_sentences()
        return sort_by_index(scores)

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
            for j in range(0, n):
                if i != j:
                    k2 = set(key_list[j])
                    interval += len(k1.intersection(k2))
            inters.append(interval)
        return sort_by_index(inters)
