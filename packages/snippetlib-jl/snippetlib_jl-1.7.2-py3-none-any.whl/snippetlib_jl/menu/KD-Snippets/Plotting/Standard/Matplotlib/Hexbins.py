# A plain hexbin-plot

fig, ax = plt.subplots(figsize=(8, 8))
scatter = ax.hexbin(x, y, cmap=plt.cm.Blues_r, gridsize=10)
ax.set_xlabel('X', fontsize=12)
ax.set_ylabel('Y', fontsize=12)
plt.tight_layout()