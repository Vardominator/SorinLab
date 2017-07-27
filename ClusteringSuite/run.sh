#!/bin/bash

for run in {1..51}
do
    python3 ClusteringSuite.py -d ../Data/luteo-1796-1798.txt -P 3,6000 -s 100000 -N feature_scale,4,5 -f 4,12 -p 4,5,6,7 -a hdbscan -r true -m 300,1000,100 -S 1
done