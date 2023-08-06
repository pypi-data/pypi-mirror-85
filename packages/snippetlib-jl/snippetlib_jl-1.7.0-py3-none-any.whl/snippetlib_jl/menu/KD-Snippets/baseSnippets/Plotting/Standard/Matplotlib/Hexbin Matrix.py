# plot a matrix of pairwise heybin-plots
# NOTE, THAT THIS ONLY WORKS ON NUMERIC DATA

plot_hist_on_diagonal = True
attributenames = data.columns

scatterdata = data[attributenames].dropna(axis=0)
# plot the scatterplot matrix
fig, ax = plt.subplots(len(attributenames), len(attributenames), figsize=(12,12))
fig.subplots_adjust(hspace=0.1, wspace=0.1)
ax = ax[::-1]
for i in range(len(attributenames)):
    for j in range(len(attributenames)):
        ax[i, j].xaxis.set_major_formatter(plt.NullFormatter())
        ax[i, j].yaxis.set_major_formatter(plt.NullFormatter())
        if plot_hist_on_diagonal:
            if i != j:
                points = ax[i, j].hexbin(scatterdata[attributenames[j]], scatterdata[attributenames[i]], cmap=plt.cm.YlGnBu_r, gridsize=10, alpha=0.8)
            else:
                ax[i, i].hist(scatterdata[attributenames[j]], alpha=0.2, histtype='stepfilled', color='k', bins=25)
        else:
            points = ax[i, j].hexbin(scatterdata[attributenames[j]], scatterdata[attributenames[i]], cmap=plt.cm.YlGnBu_r, gridsize=10, alpha=0.8)

# label the axis
for i in range(len(attributenames)):
    ax[0, i].set_xlabel(attributenames[i])
    ax[i, 0].set_ylabel(attributenames[i])