# Calculate the Locally Linear Embedding
# NOTE THAT YOUR DATA NEEDS TO BE NORMALIZED
from sklearn.manifold import LocallyLinearEmbedding

# Calculate LLE embedding
lle = LocallyLinearEmbedding(n_neighbors=20, n_components=2)
x, y = np.array(lle.fit_transform(data)).T