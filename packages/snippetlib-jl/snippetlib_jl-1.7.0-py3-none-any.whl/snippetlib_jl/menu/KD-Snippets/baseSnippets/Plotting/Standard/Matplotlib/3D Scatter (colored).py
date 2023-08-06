# A rotatable 3d scatter plot

%matplotlib notebook

scores = minmax_scale(colordata)
col = plt.cm.RdYlGn(scores)

from mpl_toolkits.mplot3d import axes3d, Axes3D
fig = plt.figure(figsize=(12,12))
ax = Axes3D(fig)
ax.set_xlabel('X', fontsize=12)
ax.set_ylabel('Y', fontsize=12)
ax.set_zlabel('Z', fontsize=12)
ax.grid(True)
ax.scatter(x, y, z, c=col, alpha=0.3, s=50)

plt.show()