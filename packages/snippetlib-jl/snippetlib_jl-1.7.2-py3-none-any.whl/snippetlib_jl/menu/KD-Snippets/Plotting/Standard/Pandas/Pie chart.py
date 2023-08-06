# Plot a pie-chart of an attribute

attribute = ''

series = data[attribute].value_counts()
series.name= ''
series.plot.pie(figsize=(6, 6), cmap='viridis', fontsize=16);