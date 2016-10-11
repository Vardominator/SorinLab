from vardoVector import squared_distance, vector_mean
import random
import itertools

import matplotlib.pyplot as mpl

class KMeans:
    """performs k-means clustering"""

    def __init__(self, k):
        self.k = k          # number of clusters
        self.means = None   # means of clusters
        
    def classify(self, input):
        """return the index of the cluster closest to the input"""
        return min(range(self.k), key=lambda i: squared_distance(input, self.means[i]))
                   
    def train(self, inputs):
    
        self.means = random.sample(inputs, self.k)
        assignments = None
        
        count = 0
        
        while True:
            # Find new assignments
            new_assignments = map(self.classify, inputs)
            
            # If no assignments have changed, we're done.
            print(self.means)
            if count == 10:           
                return

            # Otherwise keep the new assignments,
            assignments = new_assignments

            for i in range(self.k):
                i_points = [p for p, a in zip(inputs, assignments) if a == i]
                # avoid divide-by-zero if i_points is empty
                if i_points:                                
                    self.means[i] = vector_mean(i_points)

            count = count + 1


if __name__ == "__main__":
    inputs = [[-14,-5],[13,13],[20,23],[-19,-11],[-9,-16],[21,27],[-49,15],[26,13],[-46,5],[-34,-1],[11,15],[-49,0],[-22,-16],[19,28],[-12,-8],[-13,-19],[-41,8],[-11,-6],[-25,-9],[-18,-3]]

    random.seed(20) # so you get the same results as me
    clusterer = KMeans(3)
    clusterer.train(inputs)
    print("3-means:")
    print(clusterer.means)