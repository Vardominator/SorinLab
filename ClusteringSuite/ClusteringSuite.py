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
from Clustering import SESSION_MAP, PARAMS_MAP
from Partitioner import Partitioner

# DATA PROCESSING & MANIPULATION
import numpy as np
import pandas as pd
import itertools
import statistics as stat

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

# HELPER: CONVERTS LABEL ASSIGNMENTS TO COLORS
def labels_to_colors(labels):
    return [color_palette[x] if x >= 0 else (0.0, 0.0, 0.0) for x in labels]

# HELPER: CREATES PLOTS GIVEN DATA
def create_plots(dataframe, bounds, run_dir, cluster_colors):
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
parser.add_argument('-S', '--stats', default=1, type=int, help="number of runs for statistical assessment")

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
args_dict = vars(args)

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
algs_dict = dict.fromkeys(algs, {'runs': []})
now = datetime.datetime.now()
final_results = {'datetime': str(now), 'algorithms': algs_dict}
best_results = []
current_dir = ''

# CREATE MAIN RESULTS DIRECTORY IF ONE DOES EXIST
if not os.path.exists('RESULTS'):
    os.makedirs('RESULTS')

# CREATE DATA TIME DIRECTORY
datetime_dir = str(now.strftime("%Y-%m-%d__%H-%M-%S"))
current_dir = 'RESULTS/{}'.format(datetime_dir)
os.makedirs(current_dir)

# STARTING TIME
start_time = time.time()

for alg in algs:
    # current_run = {'algorithm': alg, 'results': {}}
    alg_dir = '{}/{}'.format(current_dir, alg)
    # CREATE ALGORITHM DIRECTORY
    if not os.path.exists(alg_dir):
        os.makedirs(alg_dir)

    # RETRIEVE AND EXTRACT PARAMETER ARGUMENTS
    session = SESSION_MAP[alg]()
    params = PARAMS_MAP[alg]
    # print(params)
    param_args = [args_dict[param] for param in params]

    # CREATE PARAMETERS LISTS FROM ARGUMENTS
    curr_alg_vals = []
    for param_arg in param_args:
        vals = list(map(float, param_arg.split(',')))
        if args.range is 'true':
            vals = np.arange(vals[0], vals[1] + vals[2], vals[2])
        curr_alg_vals.append(list(vals))

    # CREATE PARAMETER COMBINATIONS FOR ALGS WITH MULTIPLE PARAMS
    if len(curr_alg_vals) > 1:
        curr_alg_combos = []
        for param_comb in itertools.product(*curr_alg_vals):
            curr_alg_combos.append(list(param_comb))
        curr_alg_vals = curr_alg_combos
    else:
        curr_alg_vals = curr_alg_vals[0]

    # MULTIPLE RUNS OF ALGORITHM
    for run in range(1,args.stats + 1):
        print('Current run: {}\n'.format(run))
        run_dir = alg_dir + '/RUN_{}'.format(run)
        os.makedirs(run_dir)

        # RUN ALGORITHM FOR EACH PARAMETER COMBINATION
        for param_vals in curr_alg_vals:
            params_dict = {}
            if type(param_vals) is list:
                params_dict = dict(zip(params, param_vals))
            else:
                params_dict = {params[0]: param_vals}

            print('\tRunning {} with the following parameter(s): {}...'.format(alg, params_dict))

            param_dir = '{}/{}'.format(run_dir, ''.join(['{}_{}'.format(k,int(v)) for k,v in params_dict.items()]))
            os.mkdir(param_dir)
            
            results = session.run(dataframe, params_dict)
            
            current_run = {'parameters':params_dict, 'results': results}
            final_results['algorithms'][alg]['runs'].append(current_run)



# ENDING TIME
end_time = time.time()

# RECORD ELAPSED TIME
final_results['elapsed'] = '{}s'.format(int(end_time - start_time))

# CREATE RESULTS JSON
with open(current_dir + '/results.json', 'w') as j:
    j.write(json.dumps(final_results, sort_keys=True, indent=4))

#best_params = max(final_results[alg], key=lambda x:x['sil_score'])

hdbscan_runs = final_results['algorithms']['hdbscan']['runs']
stats = {}
results_tuples = [tuple([tuple(run['parameters'].values()), run['results']['n_clusters']]) for run in hdbscan_runs]


# EXTRACT PARAMETERS
param_set = {x[0] for x in results_tuples}
n_cluster_res = [(i, [x[1] for x in results_tuples if set(x[0]) == set(i)]) for i in param_set]
print(n_cluster_res)
n_cluster_stds = [(res[0], np.std(res[1])) for res in n_cluster_res]
n_cluster_stds = sorted(n_cluster_stds, key=lambda x:x[1])
print(n_cluster_stds)
# n_cluster_stds = tuple(dict((x[0], x) for x in n_cluster_stds).values())
# print(n_cluster_stds)



# print('Integrating results...')

# # CREATE MAIN RESULTS DIRECTORY IF ONE DOES EXIST
# if not os.path.exists('RESULTS'):
#     os.makedirs('RESULTS')

# # CREATE DIRECTORY FOR NEW RUN
# now = datetime.datetime.now()
# datetime_dir = str(now.strftime("%Y-%m-%d__%H-%M-%S"))
# current_directory = "RESULTS/" + datetime_dir
# os.makedirs(current_directory)


# with open(current_directory + '/summary.txt', 'w') as summary:

#     # PRINT FINAL RESULTS
#     summary.write('CLUSTERING SUMMARY:\n\n')

#     now_formatted = str(now.strftime("%Y-%m-%d  %H:%M:%S"))
#     summary.write('DATE & TIME COMPLETED: {}\n'.format(now_formatted))
#     summary.write('TIME ELAPSED: {}s\n\n'.format(int(end_time - start_time)))

#     filename = args.data.split('/')[-1]
#     summary.write('PREVIEW OF {}: \n\n'.format(filename))
#     summary.write(str(Partitioner().sample(dataframe, 10)))
#     summary.write('\n\n\nSAMPLE SIZE: {}'.format(args.sample))
#     summary.write('\n\n\n')

#     summary.write('METHODS USED: {}\n\n\n'.format(', '.join(algs)))

#     for alg in final_results.keys():

#         # CREATE ALGORITHM DIRECTORY
#         alg_dir = current_directory + '/{}'.format(alg)
#         os.makedirs(alg_dir)

#         summary.write('PARAMETERS CHOSEN FOR {}:\n\n'.format(alg))
#         if alg in ['hdbscan', 'dbscan']:
#             summary.write('min samples(m): \n{}'.format('\n'.join([str(m) for m in list(min_vals)])))
#             if alg is 'dbscan':
#                 summary.write('eps(e): \n{}'.format('\n'.join([str(eps) for eps in list(eps_vals)])))

#         if alg is 'kmeans':
#             summary.write('n clusters(n): \n{}'.format('\n'.join([str(n) for n in list(n_clusters_vals)])))
        
#         if args.best is True:
#             best_params = max(final_results[alg], key=lambda x:x['sil_score'])
#             best_params['algorithm'] = alg
#             best_results.append(best_params)

#             if args.range:
#                 summary.write('\n\nPARAMETERS OF {} WITH BEST SILHOUETTE SCORE: \n\n'.format(alg))
#             else:
#                 summary.write('\n\nSILHOUETTE SCORE: \n\n')

#             for item in sorted(best_params):
#                 if item not in ['labels', 'algorithm']:
#                     summary.write('{}: {}\n'.format(item, best_params[item]))

#         else:
#             for result in final_results[alg]:
#                 run_dir = current_directory + '/' + result_to_dirname(alg, result)
#                 os.makedirs(run_dir)

#         summary.write('\n\n\n')



# # CREATE RESULTS JSON
# with open(current_directory + '/results.json', 'w') as j:
#     j.write(json.dumps(final_results, sort_keys=True, indent=4))


# # CREATE PLOTS FOR BEST RESULTS
# print('Creating plots...')

# if args.fplots:
#     bounds = list(map(int, args.fplots.split(',')))
# else:
#     bounds = list(range(bounds[0], bounds[1] + 1))

# color_palette = sns.color_palette('hls', 100)


# if args.best is True:
#     for best_result in best_results:
#         cluster_colors = labels_to_colors(best_result['labels']) 
#         run_dir = current_directory + '/' + best_result['algorithm'] 
#         create_plots(dataframe, bounds, run_dir, cluster_colors)

# else:
#     for alg in final_results.keys():
#         for result in final_results[alg]:
#             cluster_colors = labels_to_colors(result['labels'])
#             run_dir = current_directory + '/' + result_to_dirname(alg, result)
#             create_plots(dataframe, bounds, run_dir, cluster_colors)

# print('Completed!')
# print('Results stored in {}/{}/'.format(os.getcwd(), current_directory))