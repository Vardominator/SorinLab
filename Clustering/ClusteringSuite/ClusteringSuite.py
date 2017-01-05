"""
    Clustering suite launching point
"""

from Partitioner import Partitioner
from Normalizer import Normalizer

import pandas as pd

import os
import argparse

parser = argparse.ArgumentParser(
    description='Welcome to the super duper awesome clustering suite!'
)

parser.add_argument("data", type=str, help="data to be clustered")

args = parser.parse_args()

dataframe = pd.read_csv(args.data, sep='\t')

# remove date(?) column -- ask Sorin about this
dataframe = dataframe.iloc[:, 0:13]
dataframe.columns = ["Proj", "Run", "Clone", "Time", "rmsd", "Rg", "S1", "S2", "L1", "L2", "T", "NC", "nonNC"]

# test Partitioner class
partitioner = Partitioner()
cleanedData = partitioner.removeAllBookkeeping(dataframe)

# test Normalizer class
normalizer = Normalizer()
normalizedData = normalizer.FeatureScale(cleanedData)


