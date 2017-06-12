import pandas as pd
import random


luteo = pd.read_csv("luteo-1796-1798.txt", sep='\t')
luteo.columns = ["Proj", "Run", "Clone", "Time", "rmsd", "Rg", "S1", "S2", "L1", "L2", "T", "NC", "nonNC"]

luteo = luteo.loc[random.sample(list(luteo.index), 100000)]
luteo = luteo.drop(luteo.columns[[0,1,2,3]], axis=1)
luteo = (luteo - luteo.min())/(luteo.max() - luteo.min())
print(luteo)

luteo.to_csv('luteo_10000_sample.csv', header=True, index=False)


# def SUBCLU(df, eps, min):
#     s_k = {}    # set of 1-D subspaces containing cluster
#     c_k = {}    # set of all sets of clusters in 1-