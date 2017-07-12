path_to_png_file = r"/home/varderes/Desktop/GitHub/SorinLab/Clustering/cityofangels"

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from kMeansClustering import KMeans


# construct new image
def recolor(pixel):
    cluster = clusterer.classify(pixel)     # index of the closest cluster
    return clusterer.means[cluster]         # mean of the closest cluster


img = mpimg.imread(path_to_png_file)

top_row = img[0]
top_left_pixel = top_row[0]
red, green, blue = top_left_pixel

# get a flattened list of all the pixels as:
pixels = [pixel for row in img for pixel in row]

# feed to clusterer
clusterer = KMeans(5, 20)
clusterer.train(pixels)

new_img = [[recolor(pixel) for pixel in row] for row in img]

plt.imshow(new_img)
plt.axis('off')
plt.show()