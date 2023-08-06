# Plot Prediction vs. Actual Value

fig, ax = plt.subplots(figsize=(6,6))
ax.scatter(reg.predict(X_test), y_test, color='k', facecolor='none', s=50, alpha=0.5)
ax.plot(ax.get_xlim(), ax.get_ylim(), ls="--", c='r')
ax.set_xlabel('Predicted Values', fontsize=12)
ax.set_ylabel('Actual Value', fontsize=12)
plt.axis('equal')
plt.tight_layout()