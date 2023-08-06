# Directly plot a line-plot of each attribute from a pandas DataFrame

data.plot.line(subplots=True, figsize=(10,8), sharex=True, cmap='viridis')
ax = plt.gca()
ax.set_xlabel('Data Record ID', fontsize=14);