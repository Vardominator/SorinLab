import numpy as np
import os
import argparse
import pandas as pd
from sklearn import metrics
from sklearn.cluster import KMeans, DBSCAN
from scipy.spatial.distance import cdist, pdist
import matplotlib.pyplot as plt

np.random.seed(42)

# retrieve input parameters & flags
parser = argparse.ArgumentParser(
    description='The Sorin kMeans script translated to Python 3.5 by Varderes Barsegyan\n\n'
)

parser.add_argument("data", type=str, help="data to be clustered")
parser.add_argument("kCount", type=int, help="Number of clusters")
parser.add_argument("outName", type=str, help="Name of the output file")
parser.add_argument("numExp", type=int, help="Number of experiements")
parser.add_argument("convCount", type=int, help="Convergence requirement")
parser.add_argument("numIters", type=int, help="Maximum number of iterations")
parser.add_argument("reassignThresh", type=int, help="Maximum number of cluster reassigns")

args = parser.parse_args()


#initialize variables
data = pd.read_csv(args.data, sep='\t')   # straight into data frame
data.columns = ["Proj", "Run", "Clone", "Time", "rmsd", "Rg", "S1", "S2", "L1", "L2",
                "T", "NC", "nonNC"]



# Select only one folding@home project
data = data.loc[data['Proj'] == 1796]

# Select only one run of that project
#data = data.loc[data['Run'] == 1]

# Select only one clone from that run
# data = data.loc[data['Clone'] <= 80]

# STARTING TIME
data = data.loc[data['Time'] >= 6000]

# Finally, select only the relevant information for clustering
data = data.iloc[:, 4:]
# sklearn kmeans parameters: n_clusters, max_iter, n_init, init, precompute_distances
print(len(data))
k_range = range(1, 50)
#k_means_var = [KMeans(n_clusters=k, init='random').fit(data) for k in k_range]
#centroids = [X.cluster_centers_ for X in k_means_var]

# kmeans = KMeans(n_clusters=30, init='random').fit(data)
# centroids = kmeans.cluster_centers_

# graphing the variance

# calculate the euclidean distance from each point to each cluster center
#k_euclid = [cdist(data, cent, 'euclidean') for cent in centroids]
#dist = [np.min(ke,axis=1) for ke in k_euclid]

# total within cluster sum of squares
#wcss = [sum(d**2) for d in dist]

# total sum of squares
#tss = sum(pdist(data)**2/data.shape[0])

# the between-cluster sum of squares
#bss = tss - wcss

# the between-cluster sum of squares
#plt.figure(1)
#plt.subplot(211)
#plt.plot(k_range, bss)

# blah = finalCentroids[:, [0, 7]]

# nativeContacts = data['NC']
# rmsd = data['rmsd']

# #plt.subplot(212)
# plt.scatter(rmsd, nativeContacts)
# clusterPoints = centroids[:, [0, 7]]
# plt.scatter(clusterPoints[:,0], clusterPoints[:,1], c='r', marker ='x', s = 20)

# print(clusterPoints)
# # plt.scatter(blah[:,0], blah[:,1], c='r', marker ='x', s = 20)

minDistance = 0.2
minSamples = 1

dbscanclustercount = 1

while minDistance <= 0.6:
    for minSamples in range(300, 700, 5):
        db = DBSCAN(eps=minDistance, min_samples=minSamples).fit(data)
        labels = db.labels_
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

        print('Min samples: ', minSamples, '; ', 'Min distances: ', minDistance)
        print(n_clusters_)
        silhouetteScore = metrics.silhouette_score(data, labels, sample_size=2000)
        print("Silhouette Coefficient: ", silhouetteScore)
        print("\n\n")

        f = open('silhouetteScores2.csv', 'a')
        f.write(str(minDistance) + ','+ str(minSamples) + ',' + str(silhouetteScore) + ',' + str(n_clusters_) + '\n')
        f.close()

        unique_labels = set(labels)
        colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))

        core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        core_samples_mask[db.core_sample_indices_] = True

        for k, col in zip(unique_labels, colors):
            if k != -1:
                #col = 'k'

                class_member_mask = (labels == k)

                xy = data[class_member_mask & ~core_samples_mask]
                plt.plot(xy['rmsd'], xy['NC'], 'o', markerfacecolor=col,
                            markeredgecolor='k', markersize=6)

                xy = data[class_member_mask & core_samples_mask]
                plt.plot(xy['rmsd'], xy['NC'], 'o', markerfacecolor=col,
                            markeredgecolor='k', markersize=14)
                            
        
        fileName = "dbscanPlots/dbscanPlot" + str(dbscanclustercount) + ".png"

        plt.savefig(fileName)

        dbscanclustercount += 1

    minDistance += 0.04


#number of clusters in labels

db = DBSCAN(eps=0.3, min_samples=450).fit(data)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
silhouetteScore = metrics.silhouette_score(data, labels, sample_size=1000)

print("Silhouette Coefficient: ", silhouetteScore)
print('Estiamted number of clusters(DBSCAN): ', n_clusters_)

unique_labels = set(labels)
colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))


for k, col in zip(unique_labels, colors):
    if k != -1:
        #col = 'k'

        class_member_mask = (labels == k)

        xy = data[class_member_mask & ~core_samples_mask]
        plt.plot(xy['rmsd'], xy['NC'], 'o', markerfacecolor=col,
                    markeredgecolor='k', markersize=6)

        xy = data[class_member_mask & core_samples_mask]
        plt.plot(xy['rmsd'], xy['NC'], 'o', markerfacecolor=col,
                    markeredgecolor='k', markersize=14)
                    



# plt.show()

plt.show()
