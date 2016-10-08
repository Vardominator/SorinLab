import numpy as np
import pandas as pd
import matplotlib.pyplot as mpl



def testRun():
    
    csvPath = "F:/GitHub/SorinLab/Clustering/freedomOfTheWorld2016.csv"
    testDF = pd.read_csv(csvPath)
    testDF = testDF.dropna()

    testDF.set_index(testDF['Countries'])

    economicSummaryIndex = testDF['EconomicFreedomSummaryIndex']
    governmentConsumption = testDF['GovernmentConsumption']

    sizeOfGovernment = testDF['SizeofGovernment']

    print(economicSummaryIndex)
    fig, ax = mpl.subplots(1)
    fig2,ax2= mpl.subplots(1)
    ax.scatter(economicSummaryIndex, governmentConsumption)
    ax.set_title("Government Consumption")
    ax2.scatter(economicSummaryIndex, sizeOfGovernment)
    ax2.set_title("Size of Government")
    mpl.show()

if __name__ == "__main__":
    testRun()