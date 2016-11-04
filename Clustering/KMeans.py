import numpy as np
import pandas as pd

class KMeans:
    
    def __init__(self, kCount, numIters):
        self.kCount = kCount
        self.numIters = numIters
        self.clusters = None

    def classify(self, input):
        """return the index of the cluster closest to the input"""
        """the index in this case is a number from 0 to kCount"""
        return min(range(self.kCount), key=lambda i: np.linalg.norm(input - self.clusters[i]))

    def train(self, data):
        """runs the kMeans algorithm"""

        # create random cluster points using argument 'kCount'
        randomRows = np.random.choice(data.index.values, self.kCount)
        self.clusters = np.array(data.ix[randomRows])

        # represent dataframe as matrix (strings => floats)
        data = data.as_matrix()

        count = 0
        assignments = None

        while count < self.numIters:
            # find new assignments: run classify method on all inputs and return a map
            #       with the cluster point assigned to each data point
            newAssignments = map(self.classify, data)

            # check for convergence: if new assignments have not changed
            if(assignments == newAssignments):
                break
            
            assignments = newAssignments

            # compute new means based on the new assignments
            for i in range(self.kCount):
                # find all points assigned to cluster i
                iPoints = [p for p, a in zip(data, assignments) if a == i]
                npiPoints = np.array(iPoints)

                # make sure iPoints is not empty
                if iPoints:
                    self.clusters[i] = npiPoints.mean(axis = 0)
                else:
                    # get a new random point
                    self.clusters[i] = data[np.random.randint(0, data.shape[0], 1)]
            
            count += 1      

