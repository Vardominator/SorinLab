import numpy as np
import pandas as pd

from sklearn.cluster import KMeans, DBSCAN
from sklearn import metrics
from scipy.spatial.distance import cdist, pdist

import datetime
import os
import time

now = datetime.datetime.now()
dateTime = str(now.strftime("%Y-%m-%d  %H:%M:%S"))
dtDirectory = str(now.strftime("%Y-%m-%d__%H-%M-%S"))

currentDirectory = ""

startTime = time.time()

class KMeans:
    def __init__(self):
        """
        Initialization can be 'random' or 'k-means++'
        """
        self.initialization = ''
        self.nClusters = 0
        self.maxIter = 0
        self.nInit = 0
        self.data = None
        
    def Run(self, data, init, nClusters, maxIter, nInit):
        self.initialization = init          # method for initialization
        self.nClusters = nClusters          # number of clusters
        self.maxIter = maxIter              # max number of iteration
        self.nInit = nInit                  # num of runs with different centroid seeds
        self.data = data
        kMeans = KMeans(init=init, n_clusters=nClusters, n_init=nInit, max_iter=maxIter).fit(data)

    def SaveResults(self, location=""):
        currentDirectory = location + "RESULTS/KMeans/" + dtDirectory
        os.makedirs(currentDirectory)

    def PlotResults(self):
        print("yo yo")

class DensityBasedScan:
    def __init__(self):
        self.labels = []
        self.nClusters = 0
        self.eps = 0
        self.minSamples = 0
        self.silhouetteScore = 0
        self.data = None

    def Run(self, data, eps, minSamples):
        self.eps = eps
        self.minSamples = minSamples
        self.data = data
        db = DBSCAN(eps=eps, min_samples=minSamples).fit(data)
        self.labels = db.labels_
        self.nClusters = len(set(self.labels)) - (1 if -1 in self.labels else 0)
        # Sample size needs to be adjusted based length of dataset
        self.silhouetteScore = metrics.silhouette_score(self.data, self.labels, sample_size=2000)

    def SaveResults(self, location=""):
        currentDirectory = location + "RESULTS/DBSCAN/" + dtDirectory
        os.makedirs(currentDirectory)

        f = open(currentDirectory + '/results.txt', 'w')
        f.write("Creation Date & Time: " + dateTime + "\n\n\n")
        f.write("Dataset preview:\n\n")
        f.write(str(self.data.head().to_string(index = False)) + "\n")
        f.write("...\n")
        f.write(str(self.data.tail().to_string(index = False)) + "\n")
        f.write("\n\n\n")
        f.write("Parameters:\n\n")
        f.write("eps: " + str(self.eps) + "\n")
        f.write("min_samples: " + str(self.minSamples) + "\n\n\n")
        f.write("Results:\n\n")
        f.write("Number of clusters: " + str(self.nClusters) + "\n")
        f.write("Silhouette score: " + str(self.silhouetteScore) + "\n\n\n")
        f.write("Elapsed time: " + str(time.time() - startTime))

        f.close()

    def PlotResults(self):
        print("yo yo")