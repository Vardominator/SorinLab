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

# Directory will be determined by the user
currentDirectory = ""

# Time logged in results file
startTime = time.time()


'''
Tasks to complete:

    1. Exception handling for desired location


'''


class KMeansSession:
    def __init__(self, version):
        # version is either 'random' or 'k-means++'
        self.version = version
        self.cluster_count = 0
        self.data = None
        self.cluster_centers = None
        self.n_init = 0
        self.n_jobs = 0

    def Run(self, data, nClusters, nInit=10, nJobs=1):
        self.data = data
        self.cluster_count = nClusters
        self.n_init = nInit
        self.n_jobs = nJobs

        kmeans = KMeans(init=self.version, n_clusters=nClusters, n_init=nInit, n_jobs=nJobs)
        kmeans.fit(data)
        self.cluster_centers = kmeans.cluster_centers_

    def SaveResults(self, location=""):
        currentDirectory = location + "RESULTS/KMeans/" + dtDirectory
        os.makedirs(currentDirectory)

        f = open(currentDirectory + '/results.txt', 'w')
        f.write("Creation Date & Time: " + dateTime + "\n\n\n")
        f.write("Dataset preview:\n\n")
        f.write(str(self.data.head().to_string(index = False)) + "\n")
        f.write("...\n")
        f.write(str(self.data.tail().to_string(index = False)) + "\n")
        f.write("\n\n\n")
        f.write("Parameters:\n\n")
        f.write("cluster_count: " + str(self.cluster_count) + "\n")
        f.write("n_init: " + str(self.n_init) + "\n")
        f.write("n_jobs: " + str(self.n_jobs) + "\n\n\n")
        

    def SavePlots(self, location=""):
        

# DBSCAN
class DBSCANSession:
    def __init__(self):
        self.labels = []
        self.nClusters = 0
        self.eps = 0
        self.minSamples = 0
        self.silhouetteScore = 0
        self.data = None
        self.core_samples_mask = None

    def Run(self, data, eps, minSamples):
        self.eps = eps
        self.minSamples = minSamples
        self.data = data
        db = DBSCAN(eps=eps, min_samples=minSamples).fit(data)
        
        # Used for plotting
        self.core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        self.core_samples_mask[db.core_sample_indices_] = True

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
        
        currentDirectory = location + "RESULTS/DBSCAN/" + dtDirectory
        # Saving plots using scheme from sklearn example

        unique_labels = set(self.labels)
        colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))


        for k, col in zip(unique_labels, colors):
            if k != - 1:
                
                class_member_mask = (labels == k)

                xy = self.data[class_member_mask & ~self.core_samples_mask]
                plt.plot(xy['rmsd'], xy['NC'], 'o', markerfacecolor=col,
                            markeredgecolor='k', markersize=6)
                
                xy = self.data[class_member_mask & self.core_samples_mask]
                plt.plot(xy['rmsd'], xy['NC'], 'o', markerfacecolor=col,
                            markeredgecolor='k', markersize=14)

        plt.savefig(currentDirectory + '/rmsd_vs_NC.png')

