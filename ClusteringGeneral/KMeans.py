import numpy as np
import pandas as pd

class KMeans:
    
    def __init__(self, kCount, numIters, reassignThresh):
        self.kCount = kCount
        self.numIters = numIters
        self.reassignThresh = reassignThresh
        self.clusters = np.zeros(kCount)
        self.clusterReassignCounts = np.zeros(kCount)

        self.averageDistBetPoints = 0

        self.finalClusterCount = 0

    def classify(self, input):
        """
        return the index of the cluster closest to the input.
        (the index in this case is a number from 0 to kCount)
        """
        return min(range(self.kCount), key=lambda i: np.linalg.norm(input - self.clusters[i]))

    def distance(self, point1, point2):
        """
        Return the distance between two points
        """
        return np.linalg.norm(point1 - point2)

    def assignedPosOkay(self, newPoint):
        """
        Check if reassigned cluster point is the same cluster point
        """
        for i in range(self.kCount):
            # check if newly assigned cluster is too close to another cluster point
            # also check if the cluster point has reached the threshold reassigned count
            #   if it has then reassignment near it is okay because that cluster will be discarded anyway
            if np.linalg.norm(newPoint - self.clusters[i]) == 0:
                return False

        return True

        # if self.clusterReassignCounts[i] < self.reassignThresh:
        #     return True;
        # else:
        #     return False


    def train(self, data):
        """
        run the kMeans algorithm
        """

        # create random cluster points using argument 'kCount'
        randomRows = np.random.choice(data.index.values, self.kCount)
        self.clusters = np.array(data.ix[randomRows])

        # represent dataframe as matrix (strings => floats)
        data = data.as_matrix()

        count = 0
        assignments = {}
        
        # mean distances used to check if reassigned cluster are near other clusters
        #   if so, they will be reassigned and it will count towards the threshold reassignment restriction
        # self.averageDistBetPoints = np.mean([self.distance(data[i], data[j]) for i in range(0, len(data) - 1) for j in range(i + 1, len(data))])
        
        # print(self.averageDistBetPoints)
        
        # print(len(data))

        # ensure no two initial cluster points are too close to each other
        # for i in range(self.kCount):
        #     if self.assignedPosOkay(self.clusters[i], i) == False:
        #         randomRow = np.random.randint(len(data), size = 1)
        #         self.clusters[i] == data[randomRow]
        #         self.clusterReassignCounts[i] += 1


        # Start kMeans algorithm
        while count < self.numIters:
            
            # hash index of data point to its assigned cluster point
            newAssignments = {}

            for i in range(len(data)):
                newAssignments[i] = self.classify(data[i])

            # check for convergence: if new assignments have not changed
            if(assignments == newAssignments):
                break
            
            assignments = newAssignments

            # compute new means based on the new assignments
            for i in range(self.kCount):
                # find all points assigned to cluster i
                
                if self.clusterReassignCounts[i] <= self.reassignThresh: 

                    iPoints = [data[j] for j in range(len(data)) if assignments[j] == i]
                    npiPoints = np.array(iPoints)
                
                    # make sure iPoints is not empty
                    if len(iPoints) > int(len(data) * 0.01):
                        self.clusters[i] = npiPoints.mean(axis = 0)
                    else:
                        self.clusterReassignCounts[i] += 1
                        
                        # Reassign the new cluster point if it is empty
                        reassignment = data[np.random.randint(0, data.shape[0], 1)]

                        # Keep reassigning if reassigned position is too close to another cluster point
                        while(self.assignedPosOkay(reassignment) == False):
                            # self.clusterReassignCounts[i] += 1
                            reassignment = data[np.random.randint(0, data.shape[0], 1)]
                        
                        self.clusters[i] = reassignment


            count += 1

            # print(self.clusterReassignCounts)
            # print("Goal: ", self.numIters, "; ", "Current(including convergence): ", count)

        # remove clusters that were reassigned more than the threshold reassignment value
        self.clusters = np.array([self.clusters[x] 
                                    for x in range(len(self.clusters)) 
                                        if self.clusterReassignCounts[x] <= self.reassignThresh])
        # print("Cluster count: ", len(self.clusters))
        self.finalClusterCount = len(self.clusters)