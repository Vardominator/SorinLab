""" 

    Algorithm for k-means clustering:

        1. Start with a set of k-means, which are points in a d-dimensional space
        2. Assign each point to the mean to which it is closest
        3. If no point's assignment has changed, stop and keep the clusters
        4. If some point's assignment has change, recompute the means and return to step 2

"""

from linear_algebra import squared_distance, vector_mean, scalar_multiply, vector_sum
import random
import matplotlib.pyplot as plt
import itertools
import pandas as pd

class KMeans:

    def __init__(self, k, iters):
        self.k = k          # number of clusters
        self.means = None   # means of clusters
        self.iters = iters  # number of iterations

    def classify(self, input):
        """return the index of the cluster closest to the input"""
        """the index in this case is a number from 0 to k"""
        return min(range(self.k), key=lambda i: squared_distance(input, self.means[i]))

    def train(self, inputs):
        # choose k random points from inputs as the initial means
        self.means = random.sample(inputs, self.k)

        count = 0
        
        while count < self.iters:
            # find new assignments; run classify method on all inputs and return a list
            assignments = map(self.classify, inputs)
            # and compute new means based on the new assignments
            for i in range(self.k):
                # find all points assigned to cluster i
                i_points = [p for p, a in zip(inputs, assignments) if a == i]

                # make sure i_points is not empty so don't divide by 0
                if i_points:
                    self.means[i] = vector_mean(i_points)
            
            count += 1


def squared_clustering_errors(inputs, k):
    """finds the total squared error from k-means clustering the inputs"""
    clusterer = KMeans(k, 20)
    clusterer.train(inputs)
    means = clusterer.means
    assignments = map(clusterer.classify, inputs)

    return sum(squared_distance(input, means[cluster])
                        for input, cluster in zip(inputs, assignments))




if __name__ == "__main__":
    
    # inputs = [[-14,-5],[13,13],[20,23],[-19,-11],[-9,-16],[21,27],[-49,15],[26,13],[-46,5],[-34,-1],[11,15],[-49,0],[-22,-16],[19,28],[-12,-8],[-13,-19],[-41,8],[-11,-6],[-25,-9],[-18,-3]]
    # print(inputs)

    # f = open('blah.txt', 'w')

    # for row in inputs:
    #     currentrow = '\t'.join(map(str,row))
    #     f.write("%s\n" % currentrow)

    # read input file into dataframe
    dataFrame = pd.read_table("blah.txt", sep='\t', lineterminator='\n', header=None)
    columns = [x for x in range(len(dataFrame.columns))]
    dataFrame.columns = columns
    clusterInputs = dataFrame.values.tolist()

    testCol1, testCol2 = zip(*clusterInputs)

    random.seed(20)
    clusterer = KMeans(3, 100)
    clusterer.train(clusterInputs)
    centroids = clusterer.means
    print(centroids)
    labels = [x for x in range(len(centroids))]

    plt.figure(1)
    plt.scatter(testCol1, testCol2)
    for label, centroid in zip(labels, centroids):
        plt.annotate(label, xy = centroid)


    # plot from 1 up to len(inputs) clusters

    ks = range(1, len(testCol1) + 1)
    errors = [squared_clustering_errors(clusterInputs, k) for k in ks]

    plt.figure(2)
    plt.plot(ks, errors)
    plt.xticks(ks)
    plt.xlabel("k")
    plt.ylabel("total squared error")
    plt.title("Total error vs. # of Clusters")


    plt.show()