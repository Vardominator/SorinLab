"""
    Protein data partitioner
"""

class Partitioner:

    # partition data by time
    def selectByTime(self, dataframe, startTime, endTime):
        dataframe = dataframe.loc[data['Time'] >= startTime]
        dataframe = dataframe.loc[data['Time'] <= endTime]
        return dataframe

    # select by project
    def selectByProject(self, dataframe, projectNumber):
        dataframe = dataframe.loc[dataframe['Proj'] == projectNumber]
        return dataframe

    # select by run
    def selectByRun(self, dataframe, runNumber):
        dataframe = dataframe.loc[dataframe['Run'] == runNumber]
        return dataframe

    # select by clone
    def selectByClone(self, dataframe, cloneNumber):
        dataframe = dataframe.loc[dataframe['Clone'] == cloneNumber]
        return dataframe

    # remove all bookkeeping data (project, run, clone, time, and date?) this is necessary for clustering
    def removeAllBookkeeping(self, dataframe, remove_native_contacts=False):
        dataframe = dataframe.iloc[:, 4:]
        if remove_native_contacts:
            dataframe = dataframe.drop('NC', 1)
        return dataframe