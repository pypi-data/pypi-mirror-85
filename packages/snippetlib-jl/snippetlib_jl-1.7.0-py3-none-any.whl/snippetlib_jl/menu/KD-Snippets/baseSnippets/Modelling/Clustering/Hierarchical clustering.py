# Calculate clusters via Hierarchical clustering (Ward)
# NOTE THAT YOUR DATA NEEDS TO BE NORMALIZED
from sklearn.neighbors import kneighbors_graph
from sklearn.cluster import AgglomerativeClustering

connectivity = kneighbors_graph(data, n_neighbors=10, include_self=False)

nClusters = 3
clus = AgglomerativeClustering(n_clusters=nClusters, linkage='ward', connectivity=connectivity)
clus.fit(data)
labels = clus.labels_.astype(float)