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
        self.kmeans = None
        self.cluster_centers = None
        self.lables = None
        self.silhouette_score = -1
        self.n_init = 0
        self.n_jobs = 0

    def Run(self, data, nClusters, nInit=10, nJobs=1):
        self.data = data
        self.cluster_count = nClusters
        self.n_init = nInit
        self.n_jobs = nJobs

        kmeans = KMeans(init=self.version, n_clusters=nClusters, n_init=nInit, n_jobs=nJobs)
        self.kmeans = kmeans
    
        kmeans.fit(data)
        self.cluster_centers = kmeans.cluster_centers_
        self.labels = kmeans.labels_

        print(self.labels)
        # self.silhouette_score = metrics.silhouette_score(self.data, self.lables, metric='euclidean', sample_size=1000)


    def SaveResults(self, location=""):
        currentDirectory = location + "RESULTS/KMeans/" + dtDirectory
        os.makedirs(currentDirectory)

        f = open(currentDirectory + '/results.txt', 'w')

        print_introduction(f, self.data)
        
        f.write("cluster_count: " + str(self.cluster_count) + "\n")
        f.write("n_init: " + str(self.n_init) + "\n")
        f.write("n_jobs: " + str(self.n_jobs) + "\n\n\n")
        f.write("Results:\n\n")
        f.write("Cluster centers:\n")
        f.write(str(self.cluster_centers) + "\n\n")

        print_ending(f, self.silhouette_score)
        
        f.close()


    def SavePlots(self, location=""):
        # Plots rmsd vs nonNC for now

        # step size of the mesh. decrease to increase the quality 
        h = 0.02

        # plot decision boundary. assign color to each
        rmsd = self.data['rmsd']    # horizontal
        nonNC = self.data['NC']  # vertical

        centroids = self.cluster_centers[:, [0, 7]]

        plt.scatter(rmsd, nonNC)
        plt.scatter(centroids[:, 0], centroids[:, 1], c='r', marker='x', s=20)

        # x_min, x_max = rmsd.min() - 1, rmsd.max() + 1
        # y_min, y_max = nonNC.min() - 1, nonNC.max() + 1
        # xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

        # Z = self.kmeans.predict(np.c_[xx.ravel(), yy.ravel()])

        # # put into color plot
        # Z = Z.reshape(xx.shape)
        # plt.figure(1)
        # plt.clf()
        # plt.imshow(Z, interpolation='nearest',
        #             extent=(xx.min(), xx.max(), yy.min(), yy.max()),
        #             cmap=plt.cm.Paired,
        #             aspect='auto', origin='lower')

        # plt.plot(rmsd, nonNC, 'k.', markersize=2)
        
        # centroids = self.cluster_centers
        # plt.scatter(centroids[:, 0], centroids[:, 7],
        #             marker='x', s=169, linewidths=3,
        #             color='w', zorder=10)

        # plt.xlim(x_min, x_max)
        # plt.ylim(y_min, y_max)
        # plt.xticks(())
        # plt.yticks(())

        # # plt.show()
        plt.savefig(currentDirectory + '/rmsd_vs_NC.png')

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

        print_introduction(f, self.data)

        f.write("eps: " + str(self.eps) + "\n")
        f.write("min_samples: " + str(self.minSamples) + "\n\n\n")
        f.write("Results:\n\n")
        f.write("Number of clusters: " + str(self.nClusters) + "\n")

        print_ending(f, self.silhouetteScore)
        
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




def print_introduction(file_handle, data):
    # Prints introduction to results
    file_handle.write("Creation Date & Time: " + dateTime + "\n\n\n")
    file_handle.write("Dataset preview:\n\n")
    file_handle.write(str(data.head().to_string(index = False)) + "\n")
    file_handle.write("...\n")
    file_handle.write(str(data.tail().to_string(index = False)) + "\n")
    file_handle.write("\n\n\n")
    file_handle.write("Parameters:\n\n")    


def print_ending(file_handle, silhouette_score):
    # Prints ending to results
    file_handle.write("Silhouette score: " + str(silhouette_score) + "\n\n\n")
    file_handle.write("Elapsed time: " + str(time.time() - startTime))