# Calculate the Multi Dimensional Scaling embedding
# NOTE THAT YOUR DATA NEEDS TO BE NORMALIZED
from sklearn.metrics.pairwise import euclidean_distances
from sklearn import manifold

# Calculate MDS embedding
dists = euclidean_distances(data, data)
dists = (dists + dists.T)/2.0

e, stress = manifold.mds.smacof(dists, n_components=2)
x, y = e.T