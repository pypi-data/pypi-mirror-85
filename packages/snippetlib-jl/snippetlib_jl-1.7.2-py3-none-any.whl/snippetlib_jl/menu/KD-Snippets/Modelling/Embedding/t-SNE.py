# Calculate the t-SNE embedding
# NOTE THAT YOUR DATA NEEDS TO BE NORMALIZED
from sklearn.manifold import TSNE

# Calculate t-SNE embedding
model = TSNE(perplexity=40, n_components=2, random_state=0)
x, y = model.fit_transform(sdata).T