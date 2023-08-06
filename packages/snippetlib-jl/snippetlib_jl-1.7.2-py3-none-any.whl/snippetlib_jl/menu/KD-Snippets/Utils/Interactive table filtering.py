# An interactive table from a Pandas.DataFrame
import qgrid
qgrid.set_grid_option('maxVisibleRows', 5)

# Edit and filter the data
qgrid_widget = qgrid.show_grid(data)
display(qgrid_widget)

# retrieve the filtered and edited data
fltered_data = qgrid_widget.get_changed_df()