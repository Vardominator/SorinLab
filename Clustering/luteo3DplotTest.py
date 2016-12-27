import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D

import pandas as pd
import numpy as np


data = pd.read_csv('luteo-1796-1798.txt', sep='\t')
data.columns = ["Proj", "Run", "Clone", "Time", "rmsd", "Rg", "S1", "S2", "L1", "L2",
                "T", "NC", "nonNC"]

data = data.loc[data['Proj'] == 1796]

data = data.loc[data['Time'] >= 6000]

data = data.loc[data['Run'] == 1]
data = data.loc[data['Clone'] <= 10]

data = data.iloc[:, 4:]

fig = plt.figure()

ax = Axes3D(fig)

X = data['rmsd']
Y = data['Rg']

Z = data['NC']

ax.scatter(X, Y, Z)

plt.show()