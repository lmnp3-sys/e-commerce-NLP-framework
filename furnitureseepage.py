"""
Le Pham
DS3500
Prof.Rachlin
HW 7 - NLP Framework
"""
import string
from collections import Counter
import matplotlib.pyplot as plt

class Furnitureseepage:
    def __init__(self):
        self.data = {} # store all processed txt here
        self.stopwords = ()

    @staticmethod
    def default_parser(text):
        """Generic parser: lcase, remove punc, extra whitespaces"""
        text = text.lower()
        text = ''.join(c for c in text if c not in string.punctuation)
        text = ' '.join(text.split())

        return text

    def load_text(self, filename, label, parser=None):
        """Load files and apply parser"""
        with open(filename, 'r', encoding='utf-8') as f:
            raw_text = f.read()

        if parser is None:
            clean_text = self.default_parser(raw_text)
        else:
            clean_text = parser(raw_text)

        words = clean_text.split()
        word_count = len(words)
        word_freq = Counter(words)

        self.data[label] = {
            'clean_text': clean_text,
            'word_count': word_count,
            'word_freq': word_freq
        }

        return self.data[label]

    def load_stop_words(self, stopfile=None):
        """Load stop words from a file"""
        with open(stopfile, "r", encoding='utf-8') as f:
            self.stopwords = set(word.strip().lower() for word in f.readlines())
        print(f"Loaded {len(self.stopwords)} stop words")

        return self.stopwords


    def wordcount_sankey(self, word_list=None, k=5):
        pass


    def visualization(self, misc_parameters):
        pass





#
# if __name__ == "__main__":
#     checker = Furnitureseepage()
#     checker.load_text("data/office_description.txt", "office")
#
#     print(f"Word count: {checker.data['office']['word_count']}")
#     print(f"Most common words: {checker.data['office']['word_freq']}")
#