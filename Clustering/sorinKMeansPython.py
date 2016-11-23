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

args = parser.parse_args()


#initialize variables
data = pd.read_csv(args.data, sep='\t')   # straight into data frame
data.columns = ["Proj", "Run", "Clone", "Time", "rmsd", "Rg", "S1", "S2", "L1", "L2",
                "T", "NC", "nonNC"]



# Select only one folding@home project
data = data.loc[data['Proj'] == 1796]

# Select only one run of that project
# data = data.loc[data['Run'] == 0]

# Select only one clone from that run
# data = data.loc[data['Clone'] == 5]

# STARTING TIME
data = data.loc[data['Time'] >= 6000]

print(data.head())

# Finally, select only the relevant information for clustering
data = data.iloc[:, 4:]

# assignment arguments to variables
kCount = args.kCount
outName = args.outName
numExp = args.numExp
convCount = args.convCount
numIters = args.numIters

# run kMeans clustering
clusterer = KMeans(kCount, numIters)
clusterer.train(data)
finalCentroids = clusterer.clusters

print(finalCentroids)



# plotting native contacts vs RMSD
nativeContacts = data['NC']
rmsd = data['rmsd']

blah = finalCentroids[:, [0, 7]]



print(blah)

plt.scatter(rmsd, nativeContacts)
plt.scatter(blah[:,0], blah[:,1], c='r', marker ='x', s = 20)

plt.show()


