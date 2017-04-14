import math
import random as rand



# VECTORS
def vector_add(v, w):
    return [v_i + w_i for v_i, w_i in zip(v, w)]

def vector_subtract(v, w):
    return [v_i - w_i for v_i, w_i in zip(v, w)]

# componentwise sum of a list of vectors: create a new vector whose first element is the sum of all the first elements
def vector_sum(vectors):
    result = vectors[0]
    for vector in vectors[1:]:
        result = vector_add(result, vector)
    return result
    
def scalar_multiply(c, v):
    return [c * v_i for v_i in v]

def vector_mean(vectors):
    n = len(vectors)
    vectSum = vector_sum(vectors)
    return scalar_multiply(1/n, vectSum)

def dot(v, w):
    return sum(v_i * w_i for v_i, w_i in zip(v,w))

def sum_of_squares(v):
    return dot(v, v)

def magnitude(v):
    return math.sqrt(sum_of_squares(v))

def squared_distance(v, w):
    return sum_of_squares(vector_subtract(v, w))

def distance(v, w):
    return magnitude(vector_subtract(v, w))


# MATRICES
def shape(A):
    num_rows = len(A)
    num_cols = len(A[0])
    return num_rows, num_cols

def get_row(A, i):
    return A[i]

def get_column(A, j):
    return [A_i[j] for A_i in A]    # jth element of row A_i for each row A_i


# create a matrix given its shape and a function for generating its elements
def make_matrix(num_rows, num_cols, entry_fn):
    return[[entry_fn(i, j)                      # given i, create a list
                    for j in range(num_cols)]   #   [entry_fn(i,0), ... ]
                    for i in range(num_rows)]   # create one list for each i

vector1 = [rand.randint(0, 3) for _ in range(10)]
vector2 = [rand.randint(0, 3) for _ in range(10)]
print([vector1, vector2])

print(scalar_multiply(5, vector1))