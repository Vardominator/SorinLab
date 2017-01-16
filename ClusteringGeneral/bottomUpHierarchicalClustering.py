"""
    Algorithm for Bottom-up Hierarchical Clustering:

        1. Make each input its own cluster of one
        2. As long as there are multiple clusters remaining,
            find the two closest clusters and merge them.

    At the end we'll have one giant cluster containing all the inputs. If we keep
        track of the merge order, we can recreate any number of clusters by unmerging.
        For example, if we want three clusters, we can just undo the last two mergest.

"""

import numpy as np
import pandas as pd

class BottomUp:
    
    """
    merged cluster will be represented as follows:

    merged = [1, [leaf1, leaf2]]
    merged = [2, [[leaf1, leaf2], [leaf1, leaf2]]
    merged = [3, [[[...]]]]

    The first value is the order of the merge. Order 1 means that there is a single cluster.
    Order n means that there are n cluster.

    The leaves in this case are the cluster points that are merged together.
    """

    def isLeaf(cluster):
        """a cluster is a leaf if it has length 1"""
        return len(cluster) == 1

    def getChildren(cluster):
        """returns the children of this cluster if it's a merged cluster;
            raises exception if this is a leaf cluster"""
        if isLeaf(cluster):
            raise TypeError("a leaf cluster has no children")
        else:
            return cluster[1]
    
    def getValues(cluster):
        """returns value(s) of the cluster"""
        if isLeaf(cluster):
            return cluster
        else:
            # for every child in cluster, retrieve the children
            return np.array([[value for value in getValues(child)] 
                                        for child in getChildren(cluster)])

    def euclidianDist(pointA, pointB):
        return np.linalg.norm(pointA - pointB)

    def clusterDistance(cluster1, cluster2, distanceAgg=min):
        """compute all pairwise distances between cluster 1 and 2
            and apply distanceAgg to the resultng list"""
        distances = np.array([[euclidianDist(p1, p2) for p1 in cluster1]
                                                        for p2 in cluster2])
        return distanceAgg(distances)

    def getMergeOrder(cluster):
        if isLeaf(cluster):
            return float('inf')
        else:
            return cluster[0]

    def bottomUpCluster(inputs, distanceAgg = min):
        cluster = np.array[inputs]

        # as long as we have more than one cluster left
        while len(cluster) > 1:
            # find the two closest clusters
            c1, c2 = min([(cluster1, cluster2)
                            [for i, cluster1 in enumerate(clusters)]
                                for cluster2 in clusters[:i]], key=lambda (x,y): clusterDistance(x, y, distanceAgg))
            
            # remove them from the list of clusters
            clusters = np.array([c for c in clusters if c != c1 and c !=c2])

            # merge them using mergeOrder
            mergedCluster = np.array(len(clusters), [c1, c2])

            # and add their merge
            clusters = np.array(clusters, mergedCluster)

        return clusters[0]