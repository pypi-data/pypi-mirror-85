# a bokeh line plot

def plot_line(data, attr):
    x = range(len(data[attr]))
    y = data[attr]
    plot = figure(plot_width=800, plot_height=400,tools="", toolbar_location=None)
    plot.xaxis.axis_label = 'Data record ID'
    plot.yaxis.axis_label = attr.replace('_', ' ').capitalize()
    
    plot.line(x, y, line_width=1, color='gray')
    
    cr = plot.circle(x, y, size=15,
                    fill_color=None, hover_fill_color="firebrick",
                    fill_alpha=0.5, hover_alpha=0.3,
                    line_color=None, hover_line_color=None)
    
    plot.add_tools(HoverTool(tooltips=None, renderers=[cr], mode='hline'))
    show(plot)

plot_line(data, 'ATTRIBUTE')