import hdbscan
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from time import gmtime, strftime

'''

Requirements:
    python 3.5+
    pip3

Python packages:
    numpy
    scipy
    sklearn
    hdbscan
    pandas
    matplotlib
    seaborn

'''

# ARGUMENT PARSER
parser = argparse.ArgumentParser(
	description = 'HDBSCAN Clustering Suite'	
)

# ARGUMENTS
parser.add_argument('-d', '--data', type=str, help="data to be clustered")
parser.add_argument('-m', '--min', type=int, help="minimum number of samples for core points")
parser.add_argument('-f', '--frange', nargs='?', type=str, help="feature space to be clustered, indexing starts at 0")
parser.add_argument('-p', '--fplots', nargs='?', type=str, help="clustered features to plot")
args = parser.parse_args()

# LOAD DATA INTO PANDAS DATAFRAME
data = pd.read_csv(args.data, sep="\s+", header=None)

# PARTITION COLUMNS OF INTEREST
if args.frange:
    bounds = list(map(int, args.frange.split(',')))
    data = data.iloc[:, bounds[0]:(bounds[1] + 1)]

# RUN HDBSCAN
clusterer = hdbscan.HDBSCAN(min_cluster_size=args.min)
cluster_labels = clusterer.fit_predict(data)

color_palette = sns.color_palette('hls', 10)
cluster_colors = [color_palette[x] if x >= 0
                  else (0.5, 0.5, 0.5)
                  for x in clusterer.labels_]

# SET UP RESULTS
if not os.path.exists('RESULTS'):
    os.makedirs('RESULTS')
result_dir = strftime("%Y-%m-%d__%H-%M-%S", gmtime())
os.makedirs('RESULTS/{}'.format(result_dir))

# CREATE AND SAVE PLOTS
plot_cols = list(map(int, args.fplots.split(',')))
for x in range(len(plot_cols)):
    for y in range(x + 1, len(plot_cols)):
        colx = bounds[0] + x
        coly = bounds[0] + y
        fig, ax = plt.subplots(1)
        ax.set_title('{} vs {}'.format(colx, coly))
        ax.scatter(data.iloc[:, x], data.iloc[:, y], s=50, linewidth=0, c=cluster_colors, alpha=0.25)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        plt.setp(ax.get_xticklabels(), visible=False)
        plt.setp(ax.get_yticklabels(), visible=False)
        plot_filename = 'RESULTS/{}/{}_vs_{}.png'.format(result_dir, colx, coly)
        fig.savefig(plot_filename)
