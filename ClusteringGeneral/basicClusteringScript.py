import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random as rand
import vardoVector as vect

from kMeansClustering import KMeans

def testRun():


    csvPath = "/home/varderes/Desktop/GitHub/SorinLab/Clustering/freedomOfTheWorld2016.csv"
    testDF = pd.read_csv(csvPath)
    testDF = testDF.dropna()

    testDF.set_index(testDF['Countries'])

    economicSummaryIndex = testDF['EconomicFreedomSummaryIndex']

    governmentConsumption = testDF['GovernmentConsumption']
    sizeOfGovernment = testDF['SizeofGovernment']
    businessRegulation = testDF['Businessregulations']
    regulation = testDF['Regulation']
    bureaucracycosts = testDF['Bureaucracycosts']
    licensingrestrictions = testDF['Licensingrestrictions']

    # fig, axes = plt.subplots(nrows=2, ncols=2)

    # axes[0,0].scatter(governmentConsumption, economicSummaryIndex)
    # axes[0,0].set_title("Government Consumption")
    # axes[0,1].scatter(sizeOfGovernment, economicSummaryIndex)
    # axes[0,1].set_title("Size of Government")
    # axes[1,0].scatter(businessRegulation, economicSummaryIndex)
    # axes[1,0].set_title("Business Regulation")
    # axes[1,1].scatter(bureaucracycosts, economicSummaryIndex)
    # axes[1,1].set_title("Bureaucracy costs")
    # plt.show()

    plt.figure(1)

    blah1 = economicSummaryIndex.tolist()
    blah2 = licensingrestrictions.tolist()
    blahFinal = list(zip(blah1, blah2))
    #print(list(zip(blah1, blah2)))

    rand.seed(20)
    clusterer = KMeans(5, 100)
    clusterer.train(blahFinal)
    
    means = clusterer.means
    print(clusterer.means)
    print(len(clusterer.means))
    
    meansx, meansy = zip(*means)

    
    plt.scatter(blah1, blah2)
    plt.scatter(meansx, meansy, color='red')

    plt.show()


if __name__ == "__main__":
    testRun()



