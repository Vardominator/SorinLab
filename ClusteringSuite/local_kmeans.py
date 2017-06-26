'''
USES SKLEARN LIBRARY TO RUN KMEANS ON A SINGLE THREAD
'''

import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt

luteo_data = pd.read_csv('luteo_clean.csv')
luteo_data = luteo_data[['rmsd', 'NC']]

plt.figure(figsize=(14,8))
plt.scatter(luteo_data['rmsd'], luteo_data['NC'],
            s=10)

kmeans = KMeans(n_clusters=20, init='k-means++', n_init=5).fit(luteo_data)
centers = kmeans.cluster_centers_
plt.scatter(centers[:,0], centers[:,1],
            s=40,
            color='r')

plt.title("Clustered Luteo with 20 Centers")
plt.xlabel('RMSD')
plt.ylabel('NC')
plt.show()

with open('cluster_centers.txt', 'w') as out_file:
    for row in centers:
        for column in row:
            out_file.write('{0} '.format(column))
        out_file.write('\n')