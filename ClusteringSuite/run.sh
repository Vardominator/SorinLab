#!/bin/bash

python3 ClusteringSuite.py -d ../Data/luteo-1796-1798.txt -s 10000 -f 4,12 -N feature_scale -a hdbscan,kmeans -r true -m 50,200,50 -n 4,20,2
