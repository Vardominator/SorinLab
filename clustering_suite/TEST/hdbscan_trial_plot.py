import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('hdbscan_results.csv')
min_samples = list(map(int, list(df.columns)))
df_mean = df.mean()
df_std = df.std()

print(df_std)
fig, ax = plt.subplots()
ax.errorbar(min_samples, df_mean, yerr=df_std, fmt='-o')
plt.show()