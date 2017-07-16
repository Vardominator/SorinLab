"""
    Protein data normalizer

    source: https://en.wikipedia.org/wiki/Normalization_(statistics)
"""

def Normalize(dataframe, method):
    return function_map[method](dataframe)       

def standard_score(dataframe):
    dataframe = (dataframe - dataframe.mean()) / dataframe.std()
    return dataframe

def feature_scale(dataframe):
    dataframe = (dataframe - dataframe.min()) / (dataframe.max() - dataframe.min())
    return dataframe

def average_constant(dataframe):
    dataframe = dataframe / dataframe.mean()
    return dataframe

def average_constant_special(dataframe, L2Thresh, TertiaryThresh):
    dataframe = dataframe.loc[dataframe['L2'] > L2Thresh and dataframe['T'] > TertiaryThresh]
    dataframe = dataframe.mean()
    return dataframe

function_map = {'standard_score': standard_score,
                        'feature_scale': feature_scale,
                        'average_constant': average_constant}
