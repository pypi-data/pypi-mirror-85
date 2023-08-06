# calculate the pairwise distances between all data records
from sklearn.metrics.pairwise import euclidean_distances

dists = euclidean_distances(data, data)
dists = (dists + dists.T)/2.0 # to assure symmetry