# Directly plot a Kernel-Density-Estimation of an attribute, given another attribute from a pandas DataFrame

attribute = 'sepal_width'
given     = 'Species'

groups = data[[attribute, given]].groupby(given)
fig, ax = plt.subplots(figsize=(8,4))
ax.set_title(r'$\mathcal{F}_{(%s | %s)}$' %(attribute.replace('_', '\_'), given.replace('_', '\_')), fontsize=18)
legend_entries = []
for group in groups:
    legend_entries.append(given + ' = ' + str(group[0]))
    try:
        group[1].plot.kde(ax=ax)
    except:
        pass
ax.set_xlabel(attribute, fontsize=14)
ax.set_ylabel('Density', fontsize=14);
plt.legend(legend_entries);