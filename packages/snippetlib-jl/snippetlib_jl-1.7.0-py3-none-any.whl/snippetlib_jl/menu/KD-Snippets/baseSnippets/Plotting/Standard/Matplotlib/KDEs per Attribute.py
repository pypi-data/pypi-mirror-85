# plot a Kernel-Density-Estimation of each value, constrained on the value of a categorical attribute

colors = {2:'y', 1:'g', 0:'r'}
grouped = data.groupby('label')
for attr in data.columns[:-1]:
    for key, group in grouped:
        group[attr].plot.kde(figsize=(3,1), title=attr, color=colors[key], label=key)
    ax = plt.gca()
    l = plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fancybox=True)
    l.set_title(attr, prop={'size':12, 'weight':'bold'})
    plt.show()