# a slightly beautified histogram

histAttribute = 'sepal_width'
histData = data[histAttribute].dropna(axis=0)

fig, ax = plt.subplots(figsize=(8,5))
ax.hist(histData, color='k', bins=20, alpha=0.3, histtype='stepfilled') 

# beautyfy the plot
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

plt.setp(plt.xticks()[1], rotation=-30)
ax.set_xlabel(histAttribute, fontsize=12)
ax.set_ylabel("Count", fontsize=12)
plt.tight_layout()