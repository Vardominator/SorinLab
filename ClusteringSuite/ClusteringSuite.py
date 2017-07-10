"""
    Clustering suite launching point
"""

from Normalizer import Normalizer
# from Clustering import KMeansSession, DBSCANSession

import pandas as pd
import random
import argparse

parser = argparse.ArgumentParser(
    description='Welcome to the super duper awesome clustering suite!'
)

# LOAD DATASET WITH DESIRED SAMPLE SIZE
parser.add_argument('-d', '--data', type=str, help="data to be clustered")
parser.add_argument('-s', '--sample', nargs='?', type=int, help="sample size of dataset")

# KMEANS PARAMETERS
parser.add_argument('-n', '--nclusters', type=int, help="number of clusters for kmeans")
parser.add_argument('-i', '--init', type=str, help="initialization method of kmeans(random or kmeans++)")

# DBSCAN PARAMETERS
parser.add_argument("eps", type=float, help="eps radius for core points")
# DBSCAN & HDBSCAN
parser.add_argument("min", type=int, help="min number of samples for core points")

# NORMALIZATION
parser.add_argument('-n', '--norm', nargs='?', type=str, help="normalization method")

## PARTITIONING
#parser.add_argument("part", type=str, help="partition dictionary")

# SET UP ARGS
args = parser.parse_args()

# READ DATASET WITH ARBITRARY AMOUNT OF ARGUMENTS
dataframe = pd.read_csv(args.data, sep='\s+', header=None)


if args.sample:
    dataframe = dataframe.loc[random.sample(list(dataframe.index), args.sample)]

if args.norm:
    dataframe = Normalizer().Normalize(dataframe, args.norm)


print(dataframe.head())

#partitioner = Partitioner()
#dataframe = partitioner.selectByTime(dataframe, 600, 50000)
#cleanedData = partitioner.removeAllBookkeeping(dataframe, remove_native_contacts=False)
#cleanedData = cleanedData.round(3)

# # test Normalizer class
# normalizer = Normalizer()
# normalizedData = normalizer.FeatureScale(cleanedData)

# print(normalizedData.tail())

# kmeansTest = KMeansSession('k-means++')
# kmeansTest.Run(normalizedData, 11, nJobs=10)
# kmeansTest.SaveResults()
# kmeansTest.SavePlots()

# dbscanTest = DBSCANSession()
# dbscanTest.Run(normalizedData, .35, 400)
# dbscanTest.SaveResults()
# dbscanTest.SavePlots()

