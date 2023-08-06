# Calculate clusters via K-Means clustering
# NOTE THAT YOUR DATA NEEDS TO BE NORMALIZED
from sklearn.cluster import KMeans

nClusters = 3
clus = KMeans(init='k-means++', n_clusters=nClusters, n_init=10)
clus.fit(data)
labels = clus.labels_.astype(float)