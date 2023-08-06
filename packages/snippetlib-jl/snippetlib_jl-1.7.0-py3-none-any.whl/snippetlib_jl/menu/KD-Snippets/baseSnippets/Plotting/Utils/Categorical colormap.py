# generate a colormap from categorical data

d = data['Species']
uniques = d.unique()
mapping = dict(zip(uniques, np.arange(len(uniques), dtype=float)))
myColor = plt.cm.RdYlGn(np.array([mapping[i] for i in d])/float(len(uniques)))