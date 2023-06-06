from sklearn.cluster import MeanShift
from pyclustering.cluster.xmeans import xmeans
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
import numpy as np
import vdx
import time
import math

X = np.array([[5],[4],[7]])

start = time.time()
for t in range(10000):
    clustering = MeanShift(bandwidth=2).fit(X)
    #print(clustering.labels_)
    # find the number of points in each cluster
    counts = np.bincount(clustering.labels_)
    #print(counts)
    # find the index of the max element in the counts array
    index = np.argmax(counts)
    #print(index)
    # find the center of the cluster with the max index
    center = clustering.cluster_centers_[index]
    #print(center)
    # find the point in X that is closest to the center
    closest = np.argmin(np.linalg.norm(X - center, axis=1))
print(X[closest])
end = time.time()
print("done in " + str(end - start) + " seconds")

start = time.time()
for t in range(10000):
    output = []
    for i in range(len(X[0])):
        input = []
        for j in range(len(X)):
            input.append(X[j][i])
        #print("input: " + str(input))
        error = 0.1
        vote = vdx.majority_voting_bootstrapping(input, error)
        vote = vdx.nearest_neighbor(vote, input)
        output.append(vote)
# find the point in X that is closest to the center
closest = np.argmin(np.linalg.norm(X - output, axis=1))
print(X[closest])
end = time.time()
print("done in " + str(end - start) + " seconds")

# The grouping algorithm is O(n * t*log(t)) Where n is the number of dimensions,
# and t is the number of modules. However, in the experiments, it behaves as O(n * t).

# The clustering algorithm is O(n*log(n) * t) Where n is the number of dimensions,
# and t is the number of modules. However, in the experiments, it behaves as O(t).

# That said, meanshift is 100 times slower in the example.

sample = np.array([[5],[4],[7]])
#print(sample)
# Prepare initial centers - amount of initial centers defines amount of clusters from which X-Means will
# start analysis.
start = time.time()
for t in range(10000):
    amount_initial_centers = 2
    initial_centers = kmeans_plusplus_initializer(sample, amount_initial_centers).initialize()
    # Create instance of X-Means algorithm. The algorithm will start analysis from 2 clusters, the maximum
    # number of clusters that can be allocated is 20.
    xmeans_instance = xmeans(sample, initial_centers, 20)
    xmeans_instance.process()
    # Extract clustering results: clusters and their centers
    clusters = xmeans_instance.get_clusters()
    #print(clusters)
    centers = xmeans_instance.get_centers()
    #print(centers)
    # Get the index of the cluster with the most points
    
    max_length = 0
    max_index = 0
    for i in range(len(clusters)):
        if len(clusters[i]) > max_length:
            max_length = len(clusters[i])
            max_index = i
    # Get the center of the cluster with the most points
    center = centers[max_index]
    #print(center)
    min_distance = math.inf
    # Get the index of the point in the sample that is closest to the center
    for i in range(len(clusters[max_index])):
        distance = math.dist(sample[clusters[max_index][i]], center)
        if distance < min_distance:
            min_distance = distance
            min_index = clusters[max_index][i]
print(sample[min_index])

end = time.time()
print("done in " + str(end - start) + " seconds")

