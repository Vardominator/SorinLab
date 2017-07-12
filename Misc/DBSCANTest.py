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
data = data.loc[data['Clone'] <= 80]

# STARTING TIME
data = data.loc[data['Time'] >= 6000]

# Finally, select only the relevant information for clustering
data = data.iloc[:, 4:]
# sklearn kmeans parameters: n_clusters, max_iter, n_init, init, precompute_distances
print(len(data))
k_range = range(1, 50)


minDistance = 0.46
minSamples = 111
print(minDistance)
print(minSamples)

db = DBSCAN(eps=minDistance, min_samples=minSamples).fit(data)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

print(labels)

n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
silhouetteScore = metrics.silhouette_score(data, labels, sample_size=2000)

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
                    

plt.show()