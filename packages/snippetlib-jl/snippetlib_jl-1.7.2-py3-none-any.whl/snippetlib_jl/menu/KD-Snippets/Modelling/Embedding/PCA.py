# Calculate the PCA embedding
from sklearn.decomposition import PCA

# Calculate PCA embedding
pca = PCA(n_components=2)
x, y = np.array(pca.fit_transform(data)).T