# Example of a custom hover tool on a scatterplot

source = ColumnDataSource(data)
hover = HoverTool(tooltips=[("Value-1", "@Val1"),("Value-2", "@Val2"),])
fig = figure(plot_width=600, plot_height=600, tools='wheel_zoom, pan, reset')
fig.add_tools(hover)
fig.scatter(x='X', y='Y', source=source, size=10, line_alpha=0.4, fill_alpha=0.0)
show(fig)