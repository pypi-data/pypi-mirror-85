# Calculate density based clusters via DBSCAN
# NOTE THAT YOUR DATA NEEDS TO BE NORMALIZED
from sklearn.cluster import DBSCAN

clus = DBSCAN(eps=0.3, min_samples=10)
clus.fit(data)
labels = clus.labels_.astype(float)