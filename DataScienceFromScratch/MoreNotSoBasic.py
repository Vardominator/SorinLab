
from functools import partial

def exp(base, power):
    return base ** power

def two_to_the(power):
    return exp(2, power)

def multiply(x,y): return x * y

def is_even(x): return x % 2 == 0 

if __name__ == "__main__":

    # funtional tools: partially apply functions to create new functions
    two_to_the = partial(exp, 2)  # is now a function of one variable
    print(two_to_the(3))          # 8


    # use map, reduce, and filter to provide functional alternatives to list comprehensions
    products = map(multiply, [1, 2], [4, 5])    # [1 * 4, 2 * 5] = [4, 10]
    
    xs = [1,2,3,4]
    x_evens = filter(is_even, xs)

    # reduce combines the first two elements of a list, then the result with the third, and so on
    x_product = reduce(multiply, xs)



    # enumerate 
    for i, document in enumerate(documents):  # returns a tuple
        do_something(i, document)

    for i, _ in enumerate(documents): do_something(i)



    # zip and argument unpacking
    list1 = ['a', 'b', 'c']
    list2 = [1, 2, 3]
    pairs = zip(list1, list2)       # is [('a', 1), ('b', 2), ('c', 3)]

    # unzipping
    letters, numbers = zip(*pairs)