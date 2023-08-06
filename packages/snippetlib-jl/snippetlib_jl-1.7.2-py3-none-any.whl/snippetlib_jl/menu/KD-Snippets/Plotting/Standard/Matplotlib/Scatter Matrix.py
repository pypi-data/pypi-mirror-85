# plot the scatter plot matrix
sm = pd.plotting.scatter_matrix(data, alpha=0.2, figsize=(15, 15), facecolor='none', edgecolor='k', diagonal='hist')

#Change label rotation
[s.xaxis.label.set_rotation(45) for s in sm[-1]]
[s.yaxis.label.set_rotation(0) for s in sm.T[0]]

# adjust the alignement of the y-labels
[s.set_ylabel(data.columns[i], ha='right') for i,s in enumerate(sm.T[0])]

#Hide all ticks
[s.set_xticks(()) for s in sm.reshape(-1)]
[s.set_yticks(()) for s in sm.reshape(-1)]

# clear upper triangle to get rid of visual clutter
for i,s_array in enumerate(sm):
    for j, s in enumerate(s_array):
        if j > i:
            s.cla()

plt.show()