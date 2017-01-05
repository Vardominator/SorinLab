"""
    Protein data normalizer

    source: https://en.wikipedia.org/wiki/Normalization_(statistics)
"""

class Normalizer():

    def StandardScore(self, dataframe):
        dataframe = (dataframe - dataframe.mean()) / dataframe.std()
        return dataframe

    def FeatureScale(self, dataframe):
        dataframe = (dataframe - dataframe.min()) / (dataframe.max() - dataframe.min())
        return dataframe