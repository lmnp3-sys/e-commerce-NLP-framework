"""
An example of a custom domain-specific parser
"""
import string
from collections import Counter

def text_parser(filename):
    """Parser for txt files"""
    with open(filename, "r", encoding='utf-8') as f:
        raw_text = f.read()

    # Clean texts
    text = raw_text.lower()
    text = ''.join(c for c in text if c not in string.punctuation)
    text = ' '.join(text.split())

    # process
    words = text.split()
    wc = Counter(words)
    num_words = len(words)

    return {'wordcount': wc,
            'numwords': num_words,
            'raw_text': raw_text,
            'clean_text': text}
