"""
    Clustering suite launching point

    Used with Anaconda distro of Python 3.6
    
    1. Activate Anaconda environment: source activate SorinLab_env
    2. Install following packages using pip while environment is active
        a. numpy
        b. cython
        c. scikit-learn
        d. matplotlib
        e. seaborn
        f. hdbscan

"""

# HELPER CLASSES
import Normalizer as norm
from Clustering import KMeansSession, DBSCANSession, HDBSCANSession
from Partitioner import Partitioner

# DATA PROCESSING & MANIPULATION
import numpy as np
import pandas as pd
import itertools

# VISUALIZATION
import matplotlib.pyplot as plt
import seaborn as sns

# MISC
import random
import argparse
import datetime
import os
import time
import json

# HELPERS
def labels_to_colors(labels):
    return [color_palette[x] if x >= 0 else (0.0, 0.0, 0.0) for x in labels]

def result_to_dirname(alg, result):
    if alg is 'kmeans':
        cur_dir = 'n-{}'.format(result['n_clusters'])
    elif alg is 'hdbscan':
        cur_dir = 'm-{}_n-{}'.format(result['min_samples'], result['n_clusters'])
    elif alg is 'dbscan':
        cur_dir = 'm-{}_e-{}_n-{}'.format(result['min_samples'], result['eps'], result['n_clusters'])
    return alg + '/' + cur_dir

def create_plots(dataframe, bounds, run_dir):
    for pair in list(itertools.combinations(bounds, r = 2)):
        x = pair[0] - bounds[0]
        y = pair[1] - bounds[0]
        fig, ax = plt.subplots(1)
        ax.set_title('{} vs {}'.format(x + bounds[0], y + bounds[0]))
        ax.scatter(dataframe.iloc[:, x], dataframe.iloc[:, y], s=50, linewidth=0,c=cluster_colors, alpha=0.80)
        plot_filename = '{}/{}_vs_{}.png'.format(run_dir, x + bounds[0], y + bounds[0])
        fig.savefig(plot_filename)
        fig.clf()    


parser = argparse.ArgumentParser(
    description='Welcome to the super duper awesome clustering suite!'
)

# LOAD DATASET WITH DESIRED SAMPLE SIZE AND FEATURES TO BE CLUSTERED + PLOTTED
parser.add_argument('-d', '--data', type=str, help="data to be clustered")
parser.add_argument('-s', '--sample', nargs='?', type=int, help="sample size of dataset")
parser.add_argument('-f', '--frange', nargs='?', type=str, help="features to be cluster")
parser.add_argument('-p', '--fplots', nargs='?', type=str, help="clustered features to be plotted")
parser.add_argument('-c', '--cnames', nargs='?', type=str, help="feature column names")
parser.add_argument('-b', '--best', nargs='?', default=False, type=bool, help="report only best results")
parser.add_argument('-s', '--stats', default=1, type=int, help="number of runs for statistical assessment")

# NORMALIZATION
parser.add_argument('-N', '--norm', nargs='?', type=str, help="normalization method and columns to be normalized")

# SELECT ALGORITHM
parser.add_argument('-a', '--algs', type=str, help="algorithms used in clustering")

# FOR USING A RANGE OF PARAMETERS
parser.add_argument('-r', '--range', nargs='?', default=False, type=bool, help="used to run with a range of parameters with a step size")

# KMEANS PARAMETERS
parser.add_argument('-n', '--nclusters', nargs='?', type=str, help="number of clusters for kmeans")
parser.add_argument('-i', '--init', nargs='?', default='k-means++', type=str, help="initialization method of kmeans(random or k-means++)")

# DBSCAN PARAMETERS
parser.add_argument('-e', '--eps', nargs='?', type=str, help="eps radius for core points")
# DBSCAN & HDBSCAN
parser.add_argument('-m', '--min', nargs='?', type=str, help="min number of samples for core points")

# SET UP ARGS
args = parser.parse_args()

# STARTING TIME
start_time = time.time()

# READ DATASET WITH ARBITRARY AMOUNT OF ARGUMENTS
dataframe_og = pd.read_csv(args.data, sep='\s+', header=None)

print('Data loaded!')
print('Clustering initiating...')

# SAMPLE DATASET
if args.sample:
    dataframe = Partitioner().sample(dataframe_og, args.sample)

# NORMALIZE DATASET
if args.norm:
    norm_cols_str = args.norm.split(',')
    norm_cols = list(map(int, norm_cols_str[1:]))
    dataframe = norm.Normalize(dataframe, norm_cols_str[0], norm_cols)

# SELECT COLUMNS TO BE CLUSTERED
if args.frange:
    bounds = list(map(int, args.frange.split(',')))
    dataframe = Partitioner().select_by_column(dataframe, bounds)

# SET COLUMN NAMES
if args.cnames:
    dataframe.columns = args.colnames.split(',')

algs = args.algs.split(',')
final_results = {}
min_vals = []
eps_vals = []
n_clusters_vals = []
best_results = []

# RUN KMEANS
if 'kmeans' in algs:
    kmeans = KMeansSession(args.init)

    n_clusters_vals = list(map(int, args.nclusters.split(',')))

    if args.range:
        n_clusters_vals = range(n_clusters_vals[0], n_clusters_vals[1] + n_clusters_vals[2], n_clusters_vals[2])

    final_results['kmeans'] = []
    for n_clusters in n_clusters_vals:
        print('Running kmeans with n_clusters = {} ...'.format(n_clusters))
        results = kmeans.run(data=dataframe, n_clusters=n_clusters)
        final_results['kmeans'].append(results)


# RUN DBSCAN OR HDBSCAN
if any(x in ['hdbscan', 'dbscan'] for x in algs):
    # BOTH ALGORITHMS REQUIRE THE M PARAMETER
    min_vals = list(map(int, args.min.split(',')))
    # CHECK IF USING RANGE WITH STEP SIZE
    if args.range:
        min_vals = range(min_vals[0], min_vals[1] + min_vals[2], min_vals[2])

    # ONLY DBSCAN REQUIRES EPS PARAMETER
    if 'dbscan' in algs:
        final_results['dbscan'] = []
        eps_vals = list(map(float, args.eps.split(',')))
        if args.range:
            eps_vals = np.arange(eps_vals[0], eps_vals[1] + eps_vals[2], eps_vals[2])

        # RUN DBSCAN WITH ALL EPS AND M PARAMETER COMBINATIONS
        for min_val in min_vals:
            for eps_val in eps_vals:
                dbscan = DBSCANSession()
                print('Running DBSCAN with min_samples = {} and eps = {}...'.format(min_val, eps_val))
                results = dbscan.run(data=dataframe, eps=eps_val, min_samples=min_val)
                final_results['dbscan'].append(results)

    # RUN HDBSCAN WITH ALL M PARAMETERS
    if 'hdbscan' in algs:
        final_results['hdbscan'] = []
        for min_val in min_vals:
            hdbscan = HDBSCANSession()
            print('Running HDBSCAN with min_samples = {}...'.format(min_val))
            results = hdbscan.run(data=dataframe, min_samples=min_val)
            final_results['hdbscan'].append(results)


# ENDTIME
end_time = time.time()

print('Integrating results...')

# CREATE MAIN RESULTS DIRECTORY IF ONE DOES EXIST
if not os.path.exists('RESULTS'):
    os.makedirs('RESULTS')

# CREATE DIRECTORY FOR NEW RUN
now = datetime.datetime.now()
datetime_dir = str(now.strftime("%Y-%m-%d__%H-%M-%S"))
current_directory = "RESULTS/" + datetime_dir
os.makedirs(current_directory)


with open(current_directory + '/summary.txt', 'w') as summary:

    # PRINT FINAL RESULTS
    summary.write('CLUSTERING SUMMARY:\n\n')

    now_formatted = str(now.strftime("%Y-%m-%d  %H:%M:%S"))
    summary.write('DATE & TIME COMPLETED: {}\n'.format(now_formatted))
    summary.write('TIME ELAPSED: {}s\n\n'.format(int(end_time - start_time)))

    filename = args.data.split('/')[-1]
    summary.write('PREVIEW OF {}: \n\n'.format(filename))
    summary.write(str(Partitioner().sample(dataframe, 10)))
    summary.write('\n\n\nSAMPLE SIZE: {}'.format(args.sample))
    summary.write('\n\n\n')

    summary.write('METHODS USED: {}\n\n\n'.format(', '.join(algs)))

    for alg in final_results.keys():

        # CREATE ALGORITHM DIRECTORY
        alg_dir = current_directory + '/{}'.format(alg)
        os.makedirs(alg_dir)

        summary.write('PARAMETERS CHOSEN FOR {}:\n\n'.format(alg))
        if alg in ['hdbscan', 'dbscan']:
            summary.write('min samples(m): \n{}'.format('\n'.join([str(m) for m in list(min_vals)])))
            if alg is 'dbscan':
                summary.write('eps(e): \n{}'.format('\n'.join([str(eps) for eps in list(eps_vals)])))

        if alg is 'kmeans':
            summary.write('n clusters(n): \n{}'.format('\n'.join([str(n) for n in list(n_clusters_vals)])))
        
        if args.best is True:
            best_params = max(final_results[alg], key=lambda x:x['sil_score'])
            best_params['algorithm'] = alg
            best_results.append(best_params)

            if args.range:
                summary.write('\n\nPARAMETERS OF {} WITH BEST SILHOUETTE SCORE: \n\n'.format(alg))
            else:
                summary.write('\n\nSILHOUETTE SCORE: \n\n')

            for item in sorted(best_params):
                if item not in ['labels', 'algorithm']:
                    summary.write('{}: {}\n'.format(item, best_params[item]))

        else:
            for result in final_results[alg]:
                run_dir = current_directory + '/' + result_to_dirname(alg, result)
                os.makedirs(run_dir)

        summary.write('\n\n\n')



# CREATE RESULTS JSON
with open(current_directory + '/results.json', 'w') as j:
    j.write(json.dumps(final_results, sort_keys=True, indent=4))


# CREATE PLOTS FOR BEST RESULTS
print('Creating plots...')

if args.fplots:
    bounds = list(map(int, args.fplots.split(',')))
else:
    bounds = list(range(bounds[0], bounds[1] + 1))

color_palette = sns.color_palette('hls', 100)

if args.best is True:
    for best_result in best_results:
        cluster_colors = labels_to_colors(best_result['labels']) 
        run_dir = current_directory + '/' + best_result['algorithm']
        create_plots(dataframe, bounds, run_dir)

else:
    for alg in final_results.keys():
        for result in final_results[alg]:
            cluster_colors = labels_to_colors(result['labels'])
            run_dir = current_directory + '/' + result_to_dirname(alg, result)
            create_plots(dataframe, bounds, run_dir)

print('Completed!')
print('Results stored in {}/{}/'.format(os.getcwd(), current_directory))