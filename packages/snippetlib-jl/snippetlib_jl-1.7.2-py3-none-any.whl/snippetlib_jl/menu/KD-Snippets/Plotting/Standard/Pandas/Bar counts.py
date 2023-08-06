# Directly plot a bar-chart of counts from a pandas DataFrame

attribute = ''

data[attribute].value_counts().plot.bar(color='grey', fontsize=12, rot=-35)
ax = plt.gca()
ax.set_xticklabels(ax.get_xticklabels(),ha='left')
ax.set_xlabel(attribute, fontsize=14)
ax.set_ylabel('Count', fontsize=14);