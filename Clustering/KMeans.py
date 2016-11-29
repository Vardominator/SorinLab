import numpy as np
import pandas as pd

class KMeans:
    
    def __init__(self, kCount, numIters, reassignThresh):
        self.kCount = kCount
        self.numIters = numIters
        self.reassignThresh = reassignThresh
        self.clusters = np.zeros(kCount)
        self.clusterReassignCounts = np.zeros(kCount)

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
            # hash index of data point to its assigned cluster point
            newAssignments = {}
            
            for i in range(len(data)):
                newAssignments[i] = self.classify(data[i])

            # check for convergence: if new assignments have not changed
            # if(assignments == newAssignments):
            #     break
            
            assignments = newAssignments

            # compute new means based on the new assignments
            for i in range(self.kCount):
                # find all points assigned to cluster i
                
                if self.clusterReassignCounts[i] <= self.reassignThresh: 

                    iPoints = [data[j] for j in range(len(data)) if assignments[j] == i]
                    npiPoints = np.array(iPoints)
                
                    # make sure iPoints is not empty, meaning if cluster i has points assigned to it
                    if len(iPoints) > 0:
                        self.clusters[i] = npiPoints.mean(axis = 0)
                    else:
                        self.clusterReassignCounts[i] += 1                        
                        self.clusters[i] = data[np.random.randint(0, data.shape[0], 1)]


            count += 1
            print(self.clusterReassignCounts)
            print("Goal: ", self.numIters, "; ", "Current(including convergence): ", count)

        # remove clusters that were reassigned more than the threshold reassignment value
        self.clusters = np.array([self.clusters[x] 
                                    for x in range(len(self.clusters)) 
                                        if self.clusterReassignCounts[x] <= self.reassignThresh])
        print(len(self.clusters))