# Data
import numpy as np

# Intelligence
from sklearn.cluster import KMeans, DBSCAN
from sklearn import metrics
import hdbscan

# Visualization
import matplotlib.pyplot as plt

# System
import datetime
import os
import time

now = datetime.datetime.now()
dateTime = str(now.strftime("%Y-%m-%d  %H:%M:%S"))
datetime_dir = str(now.strftime("%Y-%m-%d__%H-%M-%S"))

# Directory will be determined by the user
current_directory = ""

# Time logged in results file
startTime = time.time()

# CLUSTERING INTERFACE
class ClusteringSession(object):
    def run(self, **kwargs):
        raise NotImplementedError
    def save_results(self, location):
        raise NotImplementedError
    def save_plots(self, location):
        raise NotImplementedError


# KMEANS
class KMeansSession(ClusteringSession):
    def __init__(self, version):
        # version is either 'random' or 'k-means++'
        self.version = version
        self.n_clusters = 0
        self.data = None
        self.kmeans = None
        self.cluster_centers = None
        self.lables = None
        self.silhouette_score = -1
        self.n_init = 0
        self.n_jobs = 0

    def run(self, data, n_clusters, n_init=10, n_jobs=1):
        self.data = data
        self.n_clusters = n_clusters
        self.n_init = n_init
        self.n_jobs = n_jobs

        kmeans = KMeans(init=self.version, n_clusters=n_clusters, n_init=n_init, n_jobs=n_jobs)
        self.kmeans = kmeans
    
        kmeans.fit(data)
        self.cluster_centers = kmeans.cluster_centers_
        self.labels = kmeans.labels_
        self.silhouette_score = metrics.silhouette_score(self.data, self.labels, metric='euclidean')
        return {'sil_score': self.silhouette_score,
                'n_clusters': self.n_clusters}        


    # def save_results(self, location=""):
    #     currentDirectory = location + "RESULTS/KMeans/" + dtDirectory
    #     os.makedirs(currentDirectory)

    #     f = open(currentDirectory + '/results.txt', 'w')

    #     print_introduction(f, self.data)
        
    #     f.write("cluster_count: " + str(self.cluster_count) + "\n")
    #     f.write("n_init: " + str(self.n_init) + "\n")
    #     f.write("n_jobs: " + str(self.n_jobs) + "\n\n\n")
    #     f.write("Results:\n\n")
    #     f.write("Cluster centers:\n")
    #     f.write(str(self.cluster_centers) + "\n\n")

    #     print_ending(f, self.silhouette_score)
        
    #     f.close()


    # def save_plots(self, location=""):
    #     # Plots rmsd vs nonNC for now

    #     # step size of the mesh. decrease to increase the quality 
    #     h = 0.02

    #     # plot decision boundary. assign color to each
    #     rmsd = self.data['rmsd']    # horizontal
    #     nonNC = self.data['NC']  # vertical

    #     centroids = self.cluster_centers[:, [0, 7]]

    #     plt.scatter(rmsd, nonNC)
    #     plt.scatter(centroids[:, 0], centroids[:, 1], c='r', marker='x', s=20)

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
        # plt.savefig(currentDirectory + '/rmsd_vs_NC.png')


# DBSCAN
class DBSCANSession(ClusteringSession):
    def __init__(self):
        self.labels = []
        self.n_clusters = 0
        self.eps = 0
        self.min_samples = 0
        self.silhouette_score = 0
        self.data = None
        self.core_samples_mask = None

    def run(self, data, eps, min_samples):
        self.eps = eps
        self.min_samples = min_samples
        self.data = data
        db = DBSCAN(eps=eps, min_samples=min_samples).fit(data)
        
        # Used for plotting
        self.core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        self.core_samples_mask[db.core_sample_indices_] = True

        self.labels = db.labels_
        self.n_clusters = len(set(self.labels)) - (1 if -1 in self.labels else 0)
        try:
            self.silhouette_score = metrics.silhouette_score(data, self.labels, metric='euclidean')
        except :
            self.silhouette_score = -1
        
        return {'sil_score': self.silhouette_score,
                'min_samples': self.min_samples,
                'eps': self.eps}

    # def save_results(self, location=""):
    #     currentDirectory = location + "RESULTS/DBSCAN/" + dtDirectory
    #     os.makedirs(currentDirectory)

    #     f = open(currentDirectory + '/results.txt', 'w')

    #     print_introduction(f, self.data)

    #     f.write("eps: " + str(self.eps) + "\n")
    #     f.write("min_samples: " + str(self.minSamples) + "\n\n\n")
    #     f.write("Results:\n\n")
    #     f.write("Number of clusters: " + str(self.nClusters) + "\n")

    #     print_ending(f, self.silhouetteScore)
        
    #     f.close()


    # def save_plots(self, location=""):
    #     currentDirectory = location + "RESULTS/DBSCAN/" + dtDirectory
    #     # Saving plots using scheme from sklearn example

    #     unique_labels = set(self.labels)
    #     colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))


    #     for k, col in zip(unique_labels, colors):
    #         if k != - 1:
                
    #             class_member_mask = (labels == k)

    #             xy = self.data[class_member_mask & ~self.core_samples_mask]
    #             plt.plot(xy['rmsd'], xy['NC'], 'o', markerfacecolor=col,
    #                         markeredgecolor='k', markersize=6)
                
    #             xy = self.data[class_member_mask & self.core_samples_mask]
    #             plt.plot(xy['rmsd'], xy['NC'], 'o', markerfacecolor=col,
    #                         markeredgecolor='k', markersize=14)

    #     plt.savefig(currentDirectory + '/rmsd_vs_NC.png')


# HDBSCAN
class HDBSCANSession(ClusteringSession):
    def __init__(self):
        self.labels = []
        self.min_samples = 0
        self.silhouette_score = 0
        self.data = None
        #self.core_samples_mask = None

    def run(self, data, min_samples):
        self.min_samples = min_samples
        self.data = data
        hdb = hdbscan.HDBSCAN(min_cluster_size=self.min_samples)

        try:
            labels = hdb.fit_predict(data)
            self.silhouette_score = metrics.silhouette_score(data, labels, metric='euclidean')
        except :
            self.silhouette_score = -1
        
        return {'sil_score': self.silhouette_score,
                'min_samples': self.min_samples}


    def save_results(self, location):
        return super().save_results(location)

    def save_plots(self, location=""):
        current_directory = location + "RESULTS/HDBSCAN/" + datetime_dir
        print(current_directory)
        os.makedirs(current_directory)



# def print_introduction(file_handle, data):
#     # Prints introduction to results
#     file_handle.write("Creation Date & Time: " + dateTime + "\n\n\n")
#     file_handle.write("Dataset preview:\n\n")
#     file_handle.write(str(data.head().to_string(index = False)) + "\n")
#     file_handle.write("...\n")
#     file_handle.write(str(data.tail().to_string(index = False)) + "\n")
#     file_handle.write("\n\n\n")
#     file_handle.write("Parameters:\n\n")    


# def print_ending(file_handle, silhouette_score):
#     # Prints ending to results
#     file_handle.write("Silhouette score: " + str(silhouette_score) + "\n\n\n")
#     file_handle.write("Elapsed time: " + str(time.time() - startTime))