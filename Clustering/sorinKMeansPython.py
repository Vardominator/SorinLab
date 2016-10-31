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
from linear_algebra import squared_distance, vector_mean
from KMeans import KMeans

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
# testdata
data = data.head(100)

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


