"""
    Clustering suite launching point
"""

from Partitioner import Partitioner
from Normalizer import Normalizer
# from Clustering import DBSCANSession

# from Clustering import KMeansSession, DBSCANSession

import pandas as pd

import os
import argparse

parser = argparse.ArgumentParser(
    description='Welcome to the super duper awesome clustering suite!'
)

parser.add_argument("data", type=str, help="data to be clustered")

args = parser.parse_args()
dataframe = pd.read_csv(args.data, sep='\t')

# print(pd.__version__)

# dataframe = dataframe.iloc[:, 0:13]
# dataframe.columns = ["Proj", "Run", "Clone", "Time", "rmsd", "Rg", "S1", "S2", "L1", "L2", "T", "NC", "nonNC"]

# dataframe = dataframe.sample(n=100000)

# print(dataframe.tail())

# test Partitioner class
partitioner = Partitioner()
# singleProject = partitioner.selectByProject(dataframe, 1796)
# singleRun = partitioner.selectByRun(singleProject, 1)
dataframe = partitioner.selectByTime(dataframe, 600, 50000)
# print(dataframe.sample(n=100))

cleanedData = partitioner.removeAllBookkeeping(dataframe, remove_native_contacts=False)
cleanedData = cleanedData.round(3)

print(cleanedData.head())

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

