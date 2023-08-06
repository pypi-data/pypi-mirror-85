# A colored scatter-plot with Bokeh

def scatter(x, y, colordata=[]):
    fig = figure(tools='pan,wheel_zoom,reset', plot_width=800, plot_height=600)
    
    colors='steelblue'
    if len(colordata) > 0:
        try:
            scores = (minmax_scale(colordata)*255).astype(int)
            pallette = palettes.viridis(256)
            colors = [pallette[int(i)] for i in scores] 
            
            color_mapper = LinearColorMapper(palette=pallette, low=colordata.min(), high=colordata.max())
            color_bar = ColorBar(color_mapper=color_mapper, location=(0,0), orientation='vertical')
            fig.add_layout(color_bar, 'left')
        except:
            print('Colors are not numeric, using default.')
    
    fig.scatter(x, y, color=colors, fill_alpha=0.0, line_alpha=0.5, size=7)
    show(fig)

scatter(data['Xattribute'], data['Yattribute'], data['ColorAttribute'])