"""
    Clustering suite launching point
"""

from Normalizer import Normalizer
from Clustering import KMeansSession, DBSCANSession, HDBSCANSession
from Partitioner import Partitioner

import pandas as pd
import random
import argparse

parser = argparse.ArgumentParser(
    description='Welcome to the super duper awesome clustering suite!'
)

# LOAD DATASET WITH DESIRED SAMPLE SIZE AND FEATURES TO BE CLUSTERED + PLOTTED
parser.add_argument('-d', '--data', type=str, help="data to be clustered")
parser.add_argument('-s', '--sample', nargs='?', type=int, help="sample size of dataset")
parser.add_argument('-f', '--frange', nargs='?', type=str, help="features to be cluster")
parser.add_argument('-p', '--fplots', nargs='?', type=str, help="clustered features to be plotted")
parser.add_argument('-c', '--colnames', nargs='?', type=str, help="column names")

# SELECT ALGORITHM
parser.add_argument('-a', '--alg', type=str, help="algorithm used in clustering")

# KMEANS PARAMETERS
parser.add_argument('-n', '--nclusters', nargs='?', type=int, help="number of clusters for kmeans")
parser.add_argument('-i', '--init', nargs='?', default='k-means++', type=str, help="initialization method of kmeans(random or k-means++)")

# DBSCAN PARAMETERS
parser.add_argument('-e', '--eps', nargs='?', type=float, help="eps radius for core points")
# DBSCAN & HDBSCAN
parser.add_argument('-m', '--min', nargs='?', type=int, help="min number of samples for core points")

# NORMALIZATION
parser.add_argument('-N', '--norm', nargs='?', type=str, help="normalization method")

# SET UP ARGS
args = parser.parse_args()

# READ DATASET WITH ARBITRARY AMOUNT OF ARGUMENTS
dataframe = pd.read_csv(args.data, sep='\s+', header=None)

# SAMPLE DATASET
if args.sample:
    dataframe = Partitioner().sample(dataframe, args.sample)

# SELECT COLUMNS TO BE CLUSTERED
if args.frange:
    bounds = list(map(int, args.frange.split(',')))
    dataframe = Partitioner().select_by_column(dataframe, bounds)

# SET COLUMN NAMES
if args.colnames:
    dataframe.columns = args.colnames.split(',')

# NORMALIZE DATASET
if args.norm:
    dataframe = Normalizer().Normalize(dataframe, args.norm)

# RUN KMEANS
if args.alg == 'kmeans':
    kmeans = KMeansSession(args.init)
    kmeans.run(data=dataframe, n_clusters=args.nclusters)

# RUN DBSCAN
if args.alg == 'dbscan':
    dbscan = DBSCANSession()
    dbscan.run(data=dataframe, eps=args.eps, min_samples=args.min)

# RUN HDBSCAN
if args.alg == 'hdbscan':
    hdbscan = HDBSCANSession()
    hdbscan.run(data=dataframe, min_samples=args.min)
    hdbscan.save_plots()