import json
import subprocess
import os
import datetime

# CREATE MAIN RESULTS DIRECTORY IF ONE DOES EXIST
if not os.path.exists('RESULTS'):
    os.makedirs('RESULTS')

# CREATE DIRECTORY FOR CURRENT SET OF RUNS
now = datetime.datetime.now()
datetime_dir = str(now.strftime("%Y-%m-%d__%H-%M-%S"))
current_directory = "RESULTS/" + datetime_dir
os.makedirs(current_directory)

# READ RUN CONFIG
with open('run_config.json', 'r') as f:
    config = json.load(f)

# RUN SUBPROCESSES
for run in range(config['runs']):
    proc = subprocess.Popen([
        'python3',
        'ClusteringSuite.py',
        '-d',
        str(config['data']),
        '-P',
        '{},{}'.format(config['partition']['column'], config['partition']['range']),
        '-s',
        str(config['sample']),
        '-N',
        '{},{}'.format(config['norm']['method'], ','.join([str(c) for c in config['norm']['columns']])),
        '-f',
        ','.join([str(f) for f in config['range']]),
        '-p',
        ','.join([str(p) for p in config['plot_cols']]),
        '-a',
        ','.join([str(a) for a in config['algorithms']]),
        '-r',
        str(config['parameters']['range']),
        '-m',
        ','.join([str(x) for x in config['parameters']['values']])
    ], stdout=subprocess.PIPE)


    n_clusters = proc.stdout.readline()
    
    with open(current_directory + 'hdbscan_results.csv', 'w') as f:
        f.write('{}'.format())

