# Data
import numpy as np

# Intelligence
from sklearn.cluster import KMeans, DBSCAN
from sklearn import metrics
import hdbscan

# Visualization
# import matplotlib.pyplot as plt

# System
import datetime
import os
import time
import sys
import importlib as imp
import random as rand
import shutil

sys.dont_write_bytecode = True

now = datetime.datetime.now()
dateTime = str(now.strftime("%Y-%m-%d  %H:%M:%S"))
datetime_dir = str(now.strftime("%Y-%m-%d__%H-%M-%S"))

# Directory will be determined by the user
current_directory = ""

# CLUSTERING INTERFACE
class ClusteringSession(object):
    def run(self, params, threads):
        raise NotImplementedError
    def save_results(self, location):
        raise NotImplementedError
    def save_plots(self, location):
        raise NotImplementedError


# KMEANS
class KMeansSession(ClusteringSession):
    def __init__(self):
        self.n_clusters = 0
        self.data = None
        self.kmeans = None
        self.cluster_centers = None
        self.lables = None
        self.silhouette_score = -1
        self.n_init = 0
        self.n_jobs = 0

    def run(self, data, params, threads):
        self.data = data
        self.n_clusters = int(params['nclusters'])

        kmeans = KMeans(n_clusters=self.n_clusters)
        self.kmeans = kmeans
    
        kmeans.fit(data)
        self.cluster_centers = kmeans.cluster_centers_
        self.labels = kmeans.labels_

        sample_size = 0
        if len(data) >= 20000:
            sample_size = 20000
        else:
            sample_size = len(data)
        self.silhouette_score = metrics.silhouette_score(data, self.labels, metric='euclidean', sample_size=sample_size)

        return {'sil_score': self.silhouette_score,
                'labels': self.labels.tolist(),
                'n_clusters': self.n_clusters}        


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

    def run(self, data, params, threads):
        self.eps = float(params['eps'])
        self.min_samples = int(params['min'])
        self.data = data
        db = DBSCAN(eps=self.eps, min_samples=self.min_samples).fit(data)
        
        # Used for plotting
        self.core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        self.core_samples_mask[db.core_sample_indices_] = True

        self.labels = db.labels_
        self.n_clusters = len(set(self.labels)) - (1 if -1 in self.labels else 0)

        sample_size = 0
        if len(data) >= 20000:
            sample_size = 20000
        else:
            sample_size = len(data)
        self.silhouette_score = metrics.silhouette_score(data, self.labels, metric='euclidean', sample_size=sample_size)
        
        return {'sil_score': self.silhouette_score,
                'labels': self.labels.tolist(),
                'n_clusters': self.n_clusters}


# HDBSCAN
class HDBSCANSession(ClusteringSession):
    def __init__(self):
        self.labels = []
        self.min_samples = 0
        self.silhouette_score = 0
        self.data = None
        self.n_clusters = 0
        #self.core_samples_mask = None
    
    def run(self, data, params, threads):
        self.min_samples = int(params['min'])
        self.data = data

        hdb = hdbscan.HDBSCAN(min_samples=self.min_samples, core_dist_n_jobs=threads)
        # print(hdb)
        self.labels = hdb.fit_predict(data)
        self.n_clusters = len(set(self.labels)) - 1
        
        sample_size = 0
        if len(data) >= 20000:
            sample_size = 20000
        else:
            sample_size = len(data)
        self.silhouette_score = metrics.silhouette_score(data, self.labels, metric='euclidean', sample_size=sample_size)

        del hdb
        
        return {'sil_score': self.silhouette_score,
                'n_clusters': self.n_clusters}


    def save_results(self, location):
        return super().save_results(location)

    def save_plots(self, location=""):
        current_directory = location + "RESULTS/HDBSCAN/" + datetime_dir
        print(current_directory)
        os.makedirs(current_directory)


# CLUSTER SESSION DICT
SESSION_MAP = {
    'kmeans': KMeansSession,
    'hdbscan': HDBSCANSession,
    'dbscan': DBSCANSession
}

PARAMS_MAP = {
    'kmeans': ['nclusters'],
    'hdbscan': ['min'],
    'dbscan': ['min', 'eps']
}