import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import pandas as pd


clusterCounts = pd.read_csv('clusterCountDistribution2', sep="\n", header=None)

print(np.mean(clusterCounts))
print(np.std(clusterCounts))

hist, bins = np.histogram(clusterCounts, bins=25)
print(hist)

f, ax = plt.subplots()

width = np.diff(bins)
center = (bins[:-1] + bins[1:]) / 2

ax.bar(center, hist, align='center', width=width)

meanStr = str(np.mean(clusterCounts))





plt.show()