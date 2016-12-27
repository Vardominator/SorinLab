import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D

import pandas as pd
import numpy as np

data = pd.read_csv('silhouetteScores.csv')
data.columns = ['MinDistance', 'MinSamples', 'SilScore']


fig = plt.figure()

ax = Axes3D(fig)
ax.set_zlim3d(-1,1)

X = data.iloc[:,0]
Y = data.iloc[:,1]
X, Y = np.meshgrid(X, Y)

Z = data.iloc[:,2]

print(data.loc[data['SilScore'].idxmax()])

ax.plot_surface(X, Y, Z)

plt.show()