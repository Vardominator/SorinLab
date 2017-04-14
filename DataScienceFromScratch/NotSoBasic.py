
if __name__ == "__main__":
    x = [4,1,2,3]
    y = sorted(x)
    x.sort()



    # customizing sorting
    x = sorted([-4, 1, -2, -3], key=abs, reverse=True)

    # sort words and counts from highest count to lowest
    wc = sorted(word_counts.items(), key=lambda (word, count): count, reverse=True)


    # list comprehension: transforming a list into another list by choosing
    # only certain elements, or by transforming elements, or both
    even_numbers = [x for x in range(5) if x % 2 == 0]
    squares = [x for x in range(5)]
    even_squares = [x * x for x in even_numbers]

    # turn lists into dictionaries or sets
    square_dict = { x : x * x for x in range(5) }
    square_set = { x * x for x in [1, -1]}

    # multiple fors
    pairs = [(x, y)
                for x in range(10)
                for y in range(10)]  # 100 pairs (0,0) (0, 1) ... (9, 9)

    incresing_pairs = [(x, y)
                for x in range(10)
                for y in range(x + 1, 10)]


    

    # consome yielded values one at a time until none are left:
    for i in lazy_range(10):
        do_something_with(i)
    
    lazy_evens_below_20 = (i for i in lazy_range(20) if i % 2 == 0)

# generators
def lazy_range(n):
    """produce values only as needed"""
    i = 0
    while i < n:
        yield i
        i += 1