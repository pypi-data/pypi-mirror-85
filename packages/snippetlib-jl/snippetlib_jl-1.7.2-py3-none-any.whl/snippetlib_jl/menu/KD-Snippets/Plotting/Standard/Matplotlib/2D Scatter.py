# A plain scatterplot
fig, ax = plt.subplots(figsize=(8, 8))
scatter = ax.scatter(x, y, color='k', facecolor='none', s=50, alpha=0.5)
ax.set_xlabel('X', fontsize=12)
ax.set_ylabel('Y', fontsize=12)
plt.tight_layout()