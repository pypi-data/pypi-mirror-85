# Calculate the Isometric mapping embedding
# NOTE THAT YOUR DATA NEEDS TO BE NORMALIZED
from sklearn.manifold import Isomap

# Calculate ISOMAP embedding
iso = Isomap(n_neighbors=20, n_components=2)
x, y = np.array(iso.fit_transform(data)).T
