"""
DS3500 HW 7: NLP Framework
Team members: Jiayu Zou, Le Pham, Yuwen Pan
Comparing Wayfair furniture product descriptions vs customer reviews
"""

import string
from collections import Counter
from matplotlib.pyplot import MaxNLocator

import matplotlib.pyplot as plt

try:
    import plotly.graph_objects as go  # for Sankey diagrams
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False


class Furnitureseepage:
    def __init__(self):
        """
        Initialize the framework.
        Data will be stored as:
        data[label] = {
            clean_text, tokens, word_freq,
            word_count, avg_word_length, vocab_size, ...
        }
        """
        self.data = {}
        self.stopwords = set()

    # ======= Default Preprocessing =======
    @staticmethod
    def default_parser(raw_text: str) -> str:
        """
        Generic parser for plain text files.
        - Converts to lowercase
        - Removes punctuation
        - Compresses multiple spaces
        """
        text = raw_text.lower()
        text = ''.join(c for c in text if c not in string.punctuation)
        text = ' '.join(text.split())
        return text

    def load_stop_words(self, stopfile: str):
        """
        Load stop words into a set.
        Automatically used when processing tokens.
        """
        with open(stopfile, "r", encoding="utf-8") as f:
            self.stopwords = {w.strip().lower() for w in f if w.strip()}
        print(f"Loaded {len(self.stopwords)} stop words.")

    # ======= Load & Process Text =======
    def load_text(self, filename: str, label: str, parser=None):
        """
        Load and preprocess a text file.

        Two modes:
        1) parser=None -> use default_parser; file is read inside the framework.
        2) parser=function -> parser(filename) should return a dict containing:
             { "clean_text": "...", ... }
           extra fields will be stored in the data structure.
        """
        if parser is None:
            # Standard mode: read file then apply default parser
            with open(filename, "r", encoding="utf-8") as f:
                raw_text = f.read()
            clean_text = self.default_parser(raw_text)
            extra = {}
        else:
            # Custom parser mode | parser=function
            parsed = parser(filename)
            if not isinstance(parsed, dict) or "clean_text" not in parsed:
                raise ValueError("Custom parser must return a dict containing 'clean_text'.")
            clean_text = parsed["clean_text"]
            extra = {k: v for k, v in parsed.items() if k != "clean_text"}

        # Tokenization | individual pieces of text after preprocessing
        tokens = clean_text.split()

        # Remove stopwords if available
        if self.stopwords:
            tokens = [w for w in tokens if w not in self.stopwords]

        # Basic statistics
        word_freq = Counter(tokens)
        word_count = len(tokens)
        avg_word_length = sum(len(w) for w in tokens) / word_count if word_count > 0 else 0
        vocab_size = len(word_freq)

        # Store results
        self.data[label] = {
            "clean_text": clean_text,
            "tokens": tokens,
            "word_freq": word_freq,
            "word_count": word_count,
            "avg_word_length": avg_word_length,
            "vocab_size": vocab_size,
        }

        # Store custom parser fields
        self.data[label].update(extra)

        return self.data[label]

    # ======= Visualization 1: Sankey Diagram =======
    def wordcount_sankey(self, word_list=None, k=5):
        """
        Required Visualization #1:
        Text -> Word Sankey diagram.

        word_list:
            - If None: use the union of top-k frequent words from each text.
            - Otherwise: visualize only the words provided.
        """
        if not HAS_PLOTLY:
            raise ImportError("Attention! Plotly is required for Sankey diagrams. Install via: pip install plotly")

        if not self.data:
            raise ValueError("Attention! No texts loaded. Use load_text() first.")

        # Determine which words to include
        if word_list is None:
            word_set = set()
            for info in self.data.values():
                top_k = [w for w, _ in info["word_freq"].most_common(k)]
                word_set.update(top_k)
            words = sorted(word_set)
        else:
            words = [w.lower() for w in word_list]

        # Build nodes: first text labels, then word nodes
        text_labels = list(self.data.keys())
        word_labels = words
        labels = text_labels + word_labels

        # Node index mapping
        index = {lab: i for i, lab in enumerate(labels)}

        sources, targets, values = [], [], []

        # Build links from text -> word
        for tlabel, info in self.data.items():
            freq = info["word_freq"]
            for w in words:
                count = freq.get(w, 0)
                if count > 0:
                    sources.append(index[tlabel])
                    targets.append(index[w])
                    values.append(count)

        if not values:
            raise ValueError("Attention! No overlapping words found for Sankey diagram.")

        fig = go.Figure(
            data=[
                go.Sankey(
                    node=dict(
                        pad=15,
                        thickness=15,
                        line=dict(width=0.5),
                        label=labels,
                    ),
                    link=dict(
                        source=sources,
                        target=targets,
                        value=values,
                    ),
                )
            ]
        )
        fig.update_layout(title_text="Text-to-Word Sankey Diagram", font_size=10)
        fig.show()

    # ======= Visualization 2: One Subplot per Text =======
    def wordfreq_subplots(self, top_n=7):
        """
        Required Visualization #2:
        A grid of subplots, each showing the top-N most frequent words
        for each text file.
        """
        if not self.data:
            raise ValueError("Attention! No texts loaded.")

        labels = list(self.data.keys())
        n = len(labels)

        cols = 2
        rows = n // cols
        if n % cols != 0: # if odd number, add extra row
            rows += 1

        # Create subplots
        fig, axes = plt.subplots(rows, cols, figsize=(26, 7 * rows)) # 4in/row

        if isinstance(axes, plt.Axes):
            axes = [axes]
        else:
            axes = axes.flatten() # make it a flat list

        # plot each text
        for i, label in enumerate(labels):
            freq = self.data[label]['word_freq']
            top_items = freq.most_common(top_n)

            # get words and counts
            words = []
            counts = []
            for word, count in top_items:
                words.append(word)
                counts.append(count)

            # create bar chart
            axes[i].bar(words, counts)
            axes[i].set_title(label, fontsize=12)

            axes[i].set_xticks(range(len(words)))
            axes[i].set_xticklabels(words, rotation=0, fontsize=9)
            axes[i].yaxis.set_major_locator(MaxNLocator(integer=True)) # instead of 1.5, 2,5, 3.5 -> 1, 2, 3

            axes[i].margins(x=0.08)

        # hide extra subplots
        for i in range(len(labels), len(axes)):
            axes[i].axis('off')

        plt.subplots_adjust(hspace=0.9, wspace=0.35, bottom=0.08, top=0.96, left=0.05, right=0.97)
        plt.show()

    # ======= Visualization 3: Overlay Rank–Frequency Plot =======
    def rank_frequency_overlay(self, max_rank=50):
        """
        Required Visualization #3:
        A single plot overlaying rank–frequency curves (Zipf-like)
        for all texts, enabling direct comparison.
        """
        if not self.data:
            raise ValueError("Attention! No texts loaded.")

        plt.figure(figsize=(8, 6))

        for label, info in self.data.items():
            counts = sorted(info["word_freq"].values(), reverse=True)
            if not counts:
                continue
            r = min(len(counts), max_rank)
            ranks = list(range(1, r + 1))
            freqs = counts[:r]
            plt.plot(ranks, freqs, marker="o", linewidth=1, label=label)

        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel("Rank (log scale)")
        plt.ylabel("Frequency (log scale)")
        plt.title("Rank–Frequency Overlay (Zipf Plot)")
        plt.legend()
        plt.tight_layout()
        plt.show()
