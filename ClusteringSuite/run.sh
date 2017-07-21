#!/bin/bash

python3 ClusteringSuite.py -d ../Data/luteo-1796-1798.txt -s 10000 -N feature_scale,4,5 -f 4,12 -p 4,5,6,7 -a hdbscan,kmeans,dbscan -r true -m 50,200,50 -n 20,30,2 -e 0.1,1.0,0.01 -S 3
