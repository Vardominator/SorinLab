'''
LOCAL TIMES VS SPARK TIMES PLOTTING
'''

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

with open('kmeans_local_times.txt', 'r') as local_times_file:
    local_times_data = local_times_file.readlines()

with open('kmeans_spark_times.txt', 'r') as spark_times_file:
    spark_times_data = spark_times_file.readlines()

local_times = [line.split() for line in local_times_data]
spark_times = [line.split() for line in spark_times_data]

plt.figure(figsize=(14,8))

plt.scatter([row[0] for row in local_times], [row[1] for row in local_times],
            label='Local Runs')
plt.scatter([row[0] for row in spark_times], [row[1] for row in spark_times],
            label='Spark Runs')

plt.title('KMeans: Local vs. Spark')
plt.xlabel('Cluster Centers')
plt.ylabel('Running Time(s)')

plt.legend(loc='upper left')
plt.show()