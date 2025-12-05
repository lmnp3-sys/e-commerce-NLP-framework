"""
DS3500 HW7 NLP Framework
Application File
Wayfair Furniture: Product Descriptions vs Customer Reviews
Team members: Jiayu Zou, Le Pham, Yuwen Pan
"""

from furnitureseepage import Furnitureseepage

def main():
    fs = Furnitureseepage()

    # Load stop words
    fs.load_stop_words("stop_words.txt")

    # All text files (12 total)
    all_files = [
        ("data/office_description.txt",  "Office  Description"),
        ("data/office_review1.txt",      "Office  Review 1"),
        ("data/office_review2.txt",      "Office  Review 2"),

        ("data/bedroom_description.txt", "Bedroom  Description"),
        ("data/bedroom_review1.txt",     "Bedroom  Review 1"),
        ("data/bedroom_review2.txt",     "Bedroom  Review 2"),

        ("data/kitchen_description.txt", "Kitchen  Description"),
        ("data/kitchen_review1.txt",     "Kitchen  Review 1"),
        ("data/kitchen_review2.txt",     "Kitchen  Review 2"),

        ("data/bathroom_description.txt", "Bathroom  Description"),
        ("data/bathroom_review1.txt",     "Bathroom  Review 1"),
        ("data/bathroom_review2.txt",     "Bathroom  Review 2"),
    ]

    # Load all texts into the framework
    for filename, label in all_files:
        fs.load_text(filename, label)

    # Text statistics summary
    print("<<=== TEXT SUMMARY (after stopword removal) ===>>")
    for label, info in fs.data.items():
        print(f"{label}: {info['word_count']} tokens")

    print("\n<<=== TOP 5 WORDS PER TEXT ===>>")
    for label, info in fs.data.items():
        top_5 = info["word_freq"].most_common(5)
        print(f"{label}: {top_5}")

    # Visualizations required by the assignment
    print("\nGenerating visualizations now...")

    # 1) Text -> Word Sankey diagram
    fs.wordcount_sankey(k=5)

    # 2) One big plot with subplots inside (one per text)
    fs.wordfreq_subplots(top_n=7)

    # 3) Overlay rank–frequency plot
    fs.rank_frequency_overlay(max_rank=50)


if __name__ == "__main__":
    main()
