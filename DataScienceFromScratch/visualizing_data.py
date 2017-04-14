import matplotlib.pyplot as plt
from collections import Counter


def lineChart():
    years = [1950, 1960, 1970, 1980, 1990, 2000, 2010]
    gdp = [300.2, 543.2, 1075.9, 2862.5, 5979.6, 10289.7, 14958.3]

    # create a line chart, years on x-asis, gdp on y-axis
    plt.plot(years, gdp, color ='green', marker ='o', linestyle='solid')

    # add a title
    plt.title("Nominal GDP")

    # add a label to the y-axis
    plt.ylabel("Billions of $")
    plt.show()

def barChart():
    movies = ["Annie Hall", "Ben-Hur", "Casablanca", "Gandhi", "West Side Story"]
    num_oscars = [5, 11, 3, 8, 10]

    # bars are by default width 0.8, so add 0.1 to the left coordinates
    xs = [i + 0.1 for i, _ in enumerate(movies)]

    # plot bars with left x-coordinates [xs], heights [num_oscars]
    plt.bar(xs, num_oscars)

    plt.ylabel("# of academy awards")
    plt.title("My favorite movies")

    # label x-asis with movie names at bar centers
    plt.xticks([i + 0.5 for i, _ in enumerate(movies)], movies)
    plt.show()


def histogramBarChart():
    grades = [83,95,91,87,70,0,85,82,100,67,73,77,0]
    decile = lambda grade: grade // 10 * 10 #round each grade down
    histogram = Counter(decile(grade) for grade in grades) # create dictionary of grades and grade counts
    
    # shift each bar to the left by 4, give each bar its correct height, give each bar a width of 8
    plt.bar([x - 4 for x in histogram.keys()], histogram.values(), 8)

    plt.axis([-5, 105, 0, 5])   # x-axis from -5 to 105; y-axis from 0 to 5

    plt.xticks([10 * i for i in range(11)])
    plt.xlabel("Decile")
    plt.ylabel("# of students")
    plt.title("Distribution of exam 1 grades")
    plt.show()


def lineCharts():
    variance     = [1,2,4,8,16,32,64,128,256]
    bias_squared = [256,128,64,32,16,8,4,2,1]
    total_error = [x + y for x, y in zip(variance, bias_squared)]
    # enumerate over the variance list and use the index 'i'
    xs = [i for i, _ in enumerate(variance)]
    # multiple calls to plt.plot to show multiple series on the same chart
    plt.plot(xs, variance, 'g-', label='variance')
    plt.plot(xs, bias_squared, 'r-.', label='bias squared')
    plt.plot(xs, total_error, 'b:', label='total error')

    # loc=9 means top center
    plt.legend(loc=9)
    plt.xlabel("model complexity")
    plt.title("The Bias-Variance tradoff")
    plt.show()


def scatterplots():
    friends = [ 70, 65, 72, 63, 71, 64, 60, 64, 67]
    minutes = [175, 170, 205, 120, 220, 130, 105, 145, 190]
    labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']

    plt.scatter(friends, minutes)

    # label each point
    for label, friend_count, minute_count in zip(labels, friends, minutes):
        plt.annotate(label, xy = (friend_count, minute_count), xytext=(5,-5), textcoords = 'offset points')

    plt.title("Daily Minutes vs. Number of friends")
    plt.xlabel("# of friends")
    plt.ylabel("daily minutes spent on the site")
    plt.show()


if __name__ == "__main__":
    #lineChart()
    #barChart()
    #histogramBarChart()
    #lineCharts()
    scatterplots()