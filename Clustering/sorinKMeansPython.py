#!/usr/bin/python3

'''

 Sorin's kMeans script
 Sorin & Pande, Biophys J. 88, 2472-2493 (2005)
 
 Originally written in Perl 5.10
 Translated into Python 3.5 by Varderes Barsegyan

'''

import argparse
import numpy as np


# OPTIONS               PURPOSE                     DEFAULT                 FLAG
# -------------------------------------------------------------------------------                                      
data is None          # data to be clustered        [must specify]          -data
k is None             # number of centers           [must specify]          -k
name is None          # name out output file        [must specify]          -name
numExp is None        # number of experiments       [must specify]          -nume
conv = 10             # convergence requirement     10                      -conv
n = 100               # maximum iterations          100                     -iter
knownCenters = 0      # cluster center file         optional(fitting)       -clu
mult = []             # multiplier                  optional                -mult
hold = False          # do not move centers         off(testing only)       -hold


# retrieve input parameters & flags
parser = argparse.ArgumentParser()
parser.parse_args()
