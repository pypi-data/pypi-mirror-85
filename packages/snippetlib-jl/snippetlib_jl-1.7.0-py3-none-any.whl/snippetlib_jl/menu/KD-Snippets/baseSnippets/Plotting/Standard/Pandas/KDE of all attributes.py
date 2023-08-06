# plot a KDE for each attribute

def plot_single_kde(data, attr):
    data[[attr]].plot.kde(figsize=(4,2), legend=None)
    ax = plt.gca()
    ax.set_xlim([data[attr].min(), data[attr].max()])
    ax.set_xlabel(attr, fontsize=14)
    ax.set_ylabel('Density', fontsize=14)

for attr in data.columns:
    plot_single_kde(data, attr)