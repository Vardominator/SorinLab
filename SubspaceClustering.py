import pandas as pd
import random

luteo = pd.read_csv("luteo-1796-1798.txt", sep='\t')
luteo.columns = ["Proj", "Run", "Clone", "Time", "rmsd", "Rg", "S1", "S2", "L1", "L2", "T", "NC", "nonNC"]

luteo = luteo.loc[random.sample(list(luteo.index), 10000)]

print(luteo)