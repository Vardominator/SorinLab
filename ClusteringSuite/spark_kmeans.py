'''
USES SPARK MLLIB LIBRARY TO RUN KMEANS IN A HADOOP CLUSTER
AUTOMATICALLY USES ALL RESOURCES AVAILABLE ACROSS NODES
'''

from pyspark.mllib.clustering import KMeans 
from numpy import array
import time

luteo_data = sc.textFile('/final_project/luteo_clean.csv')
parsed_data = luteo_data.map(lambda line: array([float(x) for x in line.split(',')])).cache()

with open('/usr/local/kmeans_spark_times.txt', 'w') as out_file:
    for n_clusters in range(1, 30):
        start_time = time.time()
        clusters = KMeans.train(parsed_data, n_clusters, maxIterations=100)
        end_time = time.time()
        out_file.write('{0} {1}\n'.format(n_clusters, end_time-start_time))
        print('{0} {1}\n'.format(n_clusters, end_time-start_time))