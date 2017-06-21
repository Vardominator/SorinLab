import hdbscan
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.datasets import make_blobs

blobs, labels = make_blobs(n_samples = 20000, n_features=2)
test_df = pd.DataFrame(blobs).head()
print(test_df)

luteo = pd.read_csv('luteo_100000_sample.csv')
luteo_rmsd_nc = luteo.loc[:, ['rmsd', 'NC']]
print(luteo_rmsd_nc.head())

clusterer = hdbscan.HDBSCAN(min_cluster_size=500)
cluster_labels = clusterer.fit_predict(luteo)

print(len(clusterer.labels_))

color_palette = sns.color_palette('Set2', 20)

cluster_colors = [color_palette[x] if x >= 0
                  else (0.0, 0.0, 0.0)
                  for x in clusterer.labels_]

cluster_member_colors = [sns.desaturate(x, p) for x, p in
                         zip(cluster_colors, clusterer.probabilities_)]

luteo_rmsd_nc = luteo.loc[:, ['rmsd', 'NC']]

plt.scatter(luteo.rmsd, luteo.NC, s=50, linewidth=0, c=cluster_member_colors, alpha=0.25)
plt.show()
