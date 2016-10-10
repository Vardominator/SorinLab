import numpy as np
import pandas as pd
import matplotlib.pyplot as mpl
import random as rand
import vardoVector as vect
from kMeans import KMeans

def testRun():


    csvPath = "C:/Users/barse/Desktop/Github/SorinLab/Clustering/freedomOfTheWorld2016.csv"
    testDF = pd.read_csv(csvPath)
    testDF = testDF.dropna()

    testDF.set_index(testDF['Countries'])

    economicSummaryIndex = testDF['EconomicFreedomSummaryIndex']

    governmentConsumption = testDF['GovernmentConsumption']
    sizeOfGovernment = testDF['SizeofGovernment']
    businessRegulation = testDF['Businessregulations']
    regulation = testDF['Regulation']

    fig, axes = mpl.subplots(nrows=2, ncols=2)

    axes[0,0].scatter(governmentConsumption, economicSummaryIndex)
    axes[0,0].set_title("Government Consumption")
    axes[0,1].scatter(sizeOfGovernment, economicSummaryIndex)
    axes[0,1].set_title("Size of Government")
    axes[1,0].scatter(businessRegulation, economicSummaryIndex)
    axes[1,0].set_title("Business Regulation")
    axes[1,1].scatter(regulation, economicSummaryIndex)
    axes[1,1].set_title("Regulation")
    # mpl.show()



    x = [int(i) for i in regulation]
    y = [int(i) for i in economicSummaryIndex]
    
    a = np.array([x, y])

    print(a)

    inputs = [[-14,-5],[13,13],[20,23],[-19,-11],[-9,-16],[21,27],[-49,15],[26,13],[-46,5],[-34,-1],[11,15],[-49,0],[-22,-16],[19,28],[-12,-8],[-13,-19],[-41,8],[-11,-6],[-25,-9],[-18,-3]]


    rand.seed(40) # so you get the same results as me
    clusterer = KMeans(3)
    clusterer.train(inputs)
    print("3-means:")
    print(clusterer.means)


if __name__ == "__main__":
    testRun()



