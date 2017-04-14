"""
    Protein data normalizer

    source: https://en.wikipedia.org/wiki/Normalization_(statistics)
"""

class Normalizer:

    def StandardScore(self, dataframe):
        dataframe = (dataframe - dataframe.mean()) / dataframe.std()
        return dataframe

    def FeatureScale(self, dataframe):
        dataframe = (dataframe - dataframe.min()) / (dataframe.max() - dataframe.min())
        return dataframe

    def AverageConstant(self, dataframe):
        dataframe = dataframe / dataframe.mean()
        return dataframe

    def AverageConstantSpecial(self, dataframe, L2Thresh, TertiaryThresh):
        dataframe = dataframe.loc[dataframe['L2'] > L2Thresh and dataframe['T'] > TertiaryThresh]
        dataframe = dataframe.mean()
        return dataframe