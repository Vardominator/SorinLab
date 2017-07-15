"""
    Clustering suite launching point
"""

from Normalizer import Normalizer
from Clustering import KMeansSession, DBSCANSession, HDBSCANSession
from Partitioner import Partitioner

import numpy as np
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
parser.add_argument('-a', '--algs', type=str, help="algorithms used in clustering")

# FOR USING A RANGE OF PARAMETERS
parser.add_argument('-r', '--range', nargs='?', default=False, type=bool, help="used to run with a range of parameters with a step size")

# KMEANS PARAMETERS
parser.add_argument('-n', '--nclusters', nargs='?', type=str, help="number of clusters for kmeans")
parser.add_argument('-i', '--init', nargs='?', default='k-means++', type=str, help="initialization method of kmeans(random or k-means++)")

# DBSCAN PARAMETERS
parser.add_argument('-e', '--eps', nargs='?', type=str, help="eps radius for core points")
# DBSCAN & HDBSCAN
parser.add_argument('-m', '--min', nargs='?', type=str, help="min number of samples for core points")

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


algs = args.algs.split(',')
final_results = {}


# RUN KMEANS
if 'kmeans' in algs:
    kmeans = KMeansSession(args.init)

    n_clusters_vals = list(map(int, args.nclusters.split(',')))

    if args.range:
        n_clusters_vals = range(n_clusters_vals[0], n_clusters_vals[1] + n_clusters_vals[2], n_clusters_vals[2])

    final_results['kmeans'] = []
    for n_clusters in n_clusters_vals:
        results = kmeans.run(data=dataframe, n_clusters=n_clusters)
        final_results['kmeans'].append(results)


# RUN DBSCAN OR HDBSCAN
if any(x in ['hdbscan', 'dbscan'] for x in algs):
    # BOTH ALGORITHMS REQUIRE THE M PARAMETER
    min_vals = list(map(int, args.min.split(',')))
    # CHECK IF USING RANGE WITH STEP SIZE
    if args.range:
        min_vals = range(min_vals[0], min_vals[1] + min_vals[2], min_vals[2])

    # ONLY DBSCAN REQUIRES EPS PARAMETER
    if 'dbscan' in algs:
        final_results['dbscan'] = []
        eps_vals = list(map(float, args.eps.split(',')))
        if args.range:
            eps_vals = np.arange(eps_vals[0], eps_vals[1] + eps_vals[2], eps_vals[2])

        # RUN DBSCAN WITH ALL EPS AND M PARAMETER COMBINATIONS
        for min_val in min_vals:
            for eps_val in eps_vals:
                dbscan = DBSCANSession()
                results = dbscan.run(data=dataframe, eps=eps_val, min_samples=min_val)
                final_results['dbscan'].append(results)

    # RUN HDBSCAN WITH ALL M PARAMETERS
    if 'hdbscan' in algs:
        final_results['hdbscan'] = []
        for min_val in min_vals:
            hdbscan = HDBSCANSession()
            results = hdbscan.run(data=dataframe, min_samples=min_val)
            final_results['hdbscan'].append(results)


# PRINT FINAL RESULTS
# print(final_results)

for alg in final_results.keys():
    best_params = max(final_results[alg], key=lambda x:x['sil_score'])
    print('{}: {}'.format(alg, best_params))