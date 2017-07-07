import hdbscan
import argparse
import pandas as pd

parser = argparse.ArgumentParser(
	description = 'HDBSCAN Clustering Suite'	
)

parser.add_argument("data", type=str, help="data to be clustered")

args = parser.parse_args()

data = pd.read_csv(args.data, sep="\s+", header=None)

# parse by index
print(data.iloc[:, 4:9])

clusterer = hdbscan.HDBSCAN(min_cluster_size=500)
cluster_labels = clusterer.fit_predict(data)

print(cluster_labels)

