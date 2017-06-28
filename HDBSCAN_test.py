import hdbscan
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans, DBSCAN


luteo = pd.read_csv('luteo_100000_sample.csv')
print(len(luteo))
# print(luteo.columns.values)

# HDBSCAN
# clusterer = hdbscan.HDBSCAN(min_cluster_size=500)

# DBSCAN
clusterer = DBSCAN(eps=0.3, min_samples=500)

cluster_labels = clusterer.fit_predict(luteo)


color_palette = sns.color_palette('Set2', 20)

cluster_colors = [color_palette[x] if x >= 0
                  else (0.0, 0.0, 0.0)
                  for x in clusterer.labels_]

cluster_member_colors = [sns.desaturate(x, p) for x, p in
                         zip(cluster_colors, clusterer.probabilities_)]


features = ['rmsd', 'Rg', 'NC', 'nonNC']

f, axarr = plt.subplots(4, 4)

for feature1 in features:
    for feature2 in features:
        x = features.index(feature1) - 1
        y = features.index(feature2) - 1

        if x is not y:
            axarr[x, y].set_title('{} vs {}'.format(feature1, feature2))
        else:
            axarr[x, y].set_title(feature1)

        axarr[x, y].scatter(luteo[feature1], luteo[feature2], s=50, linewidth=0, c=cluster_member_colors, alpha=0.25)
        axarr[x, y].get_xaxis().set_visible(False)
        axarr[x, y].get_yaxis().set_visible(False)

plt.setp([a.get_xticklabels() for a in axarr[0,:]], visible=False)
plt.setp([a.get_yticklabels() for a in axarr[:,1]], visible=False)
# plt.scatter(luteo['rmsd'], luteo['NC'], s=50, linewidth=0, c=cluster_member_colors, alpha=0.25)
plt.show()
