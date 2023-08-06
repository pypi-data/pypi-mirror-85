# A plain lineplot

xlabel = 'attribute'

fig, ax = plt.subplots(figsize=(8, 4))
line = ax.plot(data[xlabel], color='k')
ax.set_xlabel('count', fontsize=12)
ax.set_ylabel(xlabel, fontsize=12)

plt.tight_layout()