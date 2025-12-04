from furnitureseepage import Furnitureseepage
import pprint as pp

def main():
    fs = Furnitureseepage()

    fs.load_stop_words("stop_words.txt")

    all_files = [
        ("data/office_description.txt", "office_desc"),
        ("data/office_review1.txt", "orv1"),
        ("data/office_review2.txt", "orv2"),

        ("data/bedroom_description.txt", "bedroom_desc"),
        ("data/bedroom_review1.txt", "berv1"),
        ("data/bedroom_review2.txt", "berv2"),

        ("data/kitchen_description.txt", "kitchen_desc"),
        ("data/kitchen_review1.txt", "krv1"),
        ("data/kitchen_review2.txt", "krv2"),

        ("data/bathroom_description.txt", "bathroom_desc"),
        ("data/bathroom_review1.txt", "barv1"),
        ("data/bathroom_review2.txt", "barv2"),
    ]

    for filename, label in all_files:
        fs.load_text(filename, label)

    print("<<--SUMMARY-->>")
    for label in fs.data:
        print(f"{label}: {fs.data[label]['word_count']} words")

    # pp.pprint(fs.data)

    print("<<--SUMMARY WITH STOPWORDS REMOVED-->>")
    for label in fs.data:
        top_7 = fs.data[label]['word_freq'].most_common(5)
        print(f"{label}: {fs.data[label]['word_count']} words | Top 7: {top_7}")



main()
