# Calculate Bi-clusters via spectral clustering
# NOTE THAT YOUR DATA NEEDS TO BE NORMALIZED
from sklearn.cluster import SpectralCoclustering, SpectralBiclustering

nClusters = 3

#clus = SpectralCoclustering(n_clusters=nClusters)
clus = SpectralBiclustering(n_clusters=nClusters)
clus.fit(data)
clabel = clus.column_labels_.astype(float)
rlabel = clus.row_labels_.astype(float)