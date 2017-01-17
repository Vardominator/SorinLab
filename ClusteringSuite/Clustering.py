# Data
import numpy as np
import pandas as pd

# Intelligence
from sklearn.cluster import KMeans, DBSCAN
from sklearn import metrics
from scipy.spatial.distance import cdist, pdist

# Visualization
import matplotlib.pyplot as plt

# System
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
        print("blah KMeans")
    def Run(self, data, nClusters):
        os.makedirs("RESULTS/KMeans/" + dtDirectory)

class KMeansPlusPlus:
    def __init__(self):
        print("blah KMeans++")


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


    def SavePlots(self, location=""):
        # Saving plots using scheme from sklearn example
        
        unique_labels = set(self.labels)
        colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))

        for k, col in zip(unique_labels, colors):

