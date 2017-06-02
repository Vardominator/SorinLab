"""
Requirements:
    python 3.4+
    pip package manage
    pandas library via pip
"""


import pandas as pd

# SET SAMPLE COUNT
sample_count = 10000

# READ LUTEO DATA
luteo = pd.read_csv('luteo-1796-1798.txt', '\t')

# SAMPLE LUTEO DATA
luteo_sampled = luteo.sample(sample_count)

# WRITE SAMPLED LUTEO DATA TO FILE
luteo_sampled.to_csv('luteo-sampled-{0}.txt'.format(sample_count), sep='\t', header = False)