# plotting with a geographic map-tile provider requires web-mercator coordinates 

# instead of longitude and latitude
def lng_to_mercator(lng):
    return 6378137.0 * lng * 0.017453292519943295

def lat_to_mercator(lat):
    north = lat * 0.017453292519943295
    return 3189068.5 * np.log((1.0 + np.sin(north)) / (1.0 - np.sin(north)))


source = ColumnDataSource(data)
source.add(lng_to_mercator(data['Longitude']), 'mercator_longitude')
source.add(lat_to_mercator(data['Latitude']), 'mercator_latitude')

fig = figure(tools='pan,wheel_zoom,reset', plot_width=800, plot_height=450)
fig.add_tile(get_provider('CARTODBPOSITRON'), alpha=1.0)
fig.scatter(x='mercator_longitude', 
            y='mercator_latitude', 
            source=source, 
            size=10, 
            alpha=0.3,
            fill_color=None, 
            line_color='red')
fig.axis.visible = False
show(fig)