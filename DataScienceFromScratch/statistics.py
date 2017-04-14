from collections import Counter
from linear_algebra import sum_of_squares
import math

def length(input):
    return len(input)

def maximum(input):
    return max(input)

def minimum(input):
    return min(input)

def sortedValues(input):
    return sorted(input)
    
def mean(input):
    return mean(input) / len(input)

def median(input):
    n = len(input)
    sortedInput = sorted(input)
    midpoint = n / 2

    if(n % 2 == 1):
        return sortedInput[midpoint]

    else:
        low = midpoint - 1
        high = midpoint
        return (sorted[low] + sorted[high]) / 2


def quantile(input, p):
    """The quantile represents the value less than which a certain
        percentile of the data lies."""
    pIndex = int(p * len(input))
    return sorted(input)[pIndex]

def mode(input):
    """ returns a list of the most common value[s]"""
    counts = Counter(input)
    maxCount = max(counts.values())
    return [x_i for x_i, count in counts.iteritems() if count == maxCount]


# Dispersion refers to the measures of how spread out our data is.
# The following methods are various ways to measure dispersion.

def dataRange(input):
    return max(input) - min(input)

# calculating variance
def deMean(input):
    """translate x by subtracting its mean (so the result has ean 0)"""
    xBar = mean(input)
    return [x_i - xBar for x_i in input]

def variance(input):
    """assumes input has at least two elements"""
    n = len(input)
    deviations = deMean(input)
    return sum_of_squares(deviations) / (n - 1)
    """x_bar is an estimate of the actual mean for large populations
        therefore we divide by n-1 instead of n"""

def standardDeviation(input):
    return math.sqrt(variance(input))

def interquartileRange(input):
    """A more robust alternative is computing the difference between the
        75th percentile value and 25th percentile value. This is because
        an outlier can throw off the STD by a huge number; rendering it
        quite meaningless."""
    return quantile(input, 0.75) - quantile(input, 0.25)


# correlation: whereas variance measures how a single variable deviates from its mean,
#               covariance measures how two variables vary in tandem from their means
def covariance(x, y):
    n = len(x)
    return dot(deMean(x), deMean(y)) / (n - 1)

# correlation is hard to intepret for the following reasons: 
#   1. Its units are the products of the inputs' units, which can be hard to make sense of
#   2. If x had twice the values from the original, the covariance would be twice as large,
#       but they variables would be just as interrelated
#
# For these reasons correlation is a better measure, it divides out the standard deviations
def correlation(x, y):
    stdX = standardDeviation(x)
    stdY = standardDeviation(y)

    if(stdX > 0 and stdY > 0):
        return covariance(x, y) / (stdX * stdY)
    else:
        return 0    # if no variation, the correlation is zero


# Some more information about correlation
#
# It's best to understand so that you can check for possible confounding factors.
#
# The sort of relationship that correlation looks for is how the mean of x compares
#   to the mean of y.
#
# "Correlation is not causation"
#
# One way to feel more confident about causality is by conducting randomized trials.
