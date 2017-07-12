#!/usr/bin/python3

'''

 Sorin's kMeans script
 Sorin & Pande, Biophys J. 88, 2472-2493 (2005)
 
 Originally written in Perl 5.10
 Translated into Python 3.5 by Varderes Barsegyan

'''

import os
import argparse
import numpy as np
import pandas as pd
from KMeans import KMeans

import matplotlib.pyplot as plt

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



# # Select only one folding@home project
# data = data.loc[data['Proj'] == 1796]

# # Select only one run of that project
# #data = data.loc[data['Run'] == 0]

# # Select only one clone from that run
# data = data.loc[data['Clone'] == 1]

# # STARTING TIME
# data = data.loc[data['Time'] >= 6000]

# Finally, select only the relevant information for clustering
data = data.iloc[:, 4:]

data = (data - data.min()) / (data.max() - data.min())

# assignment arguments to variables
kCount = args.kCount
outName = args.outName
numExp = args.numExp
convCount = args.convCount
numIters = args.numIters
reassignThresh = args.reassignThresh

# run kMeans clustering
clusterer = KMeans(kCount, numIters, reassignThresh)
clusterer.train(data)
finalCentroids = clusterer.clusters

# plotting native contacts vs RMSD
nativeContacts = data['NC']
rmsd = data['rmsd']

blah = finalCentroids[:, [0, 7]]

plt.scatter(rmsd, nativeContacts)
plt.scatter(blah[:,0], blah[:,1], c='r', marker ='x', s = 20)


plt.show()


# find distribution of cluster counts

# f = open('clusterCountDistribution2', 'w')

# for i in range(1000):
    
#     print("Goal: ", 1000, "; ", "Current: ", i)

#     # assignment arguments to variables
#     kCount = args.kCount
#     outName = args.outName
#     numExp = args.numExp
#     convCount = args.convCount
#     numIters = args.numIters
#     reassignThresh = args.reassignThresh

#     # run kMeans clustering
#     clusterer = KMeans(kCount, numIters, reassignThresh)
#     clusterer.train(data)
#     finalCentroids = clusterer.clusters

#     f.write(str(clusterer.finalClusterCount) + "\n")

#     print("Current cluster count: ", clusterer.finalClusterCount)

#     # plotting native contacts vs RMSD
#     nativeContacts = data['NC']
#     rmsd = data['rmsd']

#     blah = finalCentroids[:, [0, 7]]

# f.close()

# plt.scatter(rmsd, nativeContacts)
# plt.scatter(blah[:,0], blah[:,1], c='r', marker ='x', s = 20)


# plt.show()
