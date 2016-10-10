from collections import defaultdict
from collections import Counter

if __name__ == "__main__":

    grades = {'Joel': 80, 'Tim': 85}

    print(grades['Joel'])

    # three ways to count words in a file using a dictionary

    # 1
    word_count = {}
    for word in document:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

    # 2 : try-catches
    word_count = {}
    for word in document:
        try:
            word_count[word] += 1
        except KeyError:
            word_count[word] = 1

    # 3 : using get
    word_count = {}
    for word in document:
        previous_count = word_count.get(word, 0)  # default to 0 if key is not found
        word_count[word] = previous_count + 1


    # * : using defaultdict: takes care of missing keys automagically 
    word_count = defaultdict(int)
    for word in document:
        word_count[word] += 1

    # **: using Counter
    word_count = Counter(document)



    #print the 10 most common words and their counts
    for word, count in word_count.most_common(10):
        print(word, count)