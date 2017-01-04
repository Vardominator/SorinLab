"""
    Protein data partitioner
"""

import pandas as pd

class Partitioner:

    # load data set and set column names 
    def __init__(self, datasetPath):
        self.data = pd.read_csv(datasetPath) 
        self.data.columns = ["Proj", "Run", "Clone", "Time", "rmsd", "Rg", "S1", "S2", "L1", "L2",
                "T", "NC", "nonNC"]

    # partition data by time
    def selectByTime(self, startTime=0, endTime=data['Time'].iloc[-1]):
        data = data.loc[data['Time'] >= startTime]
        data = data.loc[data['Time'] <= endTime]

    
    # select by project
    def selectByProject(self, projectNumber):
        data = data.loc[data['Proj'] == projectNumber]

    # select by run
    def selectByRun(self, runNumber):
        data = data.loc[data['Run'] == runNumber]

    # select by clone
    def selectByClone(self, cloneNumber):
        data = data.loc[data['Clone'] == cloneNumber]

    # remove all bookkeeping data (project, run, clone, and time) this is necessary for clustering
    def removeAllBookkeeping(self):
        data = data.iloc[:, 4:]


