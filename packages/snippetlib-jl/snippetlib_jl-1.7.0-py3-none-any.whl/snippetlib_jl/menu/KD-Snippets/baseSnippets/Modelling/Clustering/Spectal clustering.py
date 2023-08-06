# Calculate clusters via Spectral clustering
# NOTE THAT YOUR DATA NEEDS TO BE NORMALIZED
from sklearn.cluster import SpectralClustering

nClusters = 3
clus = SpectralClustering(n_clusters=nClusters, affinity="nearest_neighbors")
clus.fit(data)
labels = clus.labels_.astype(float)