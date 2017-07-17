#!/bin/bash

python ClusteringSuite.py -d ../Data/luteo-1796-1798.txt -s 10000 -f 4,12 -N feature_scale -a hdbscan -r true -m 30,60,10
