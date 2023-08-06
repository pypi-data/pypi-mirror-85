# a sortable Bokeh table. Nice for a dashboard
from bokeh.models.widgets import DataTable, TableColumn

source = ColumnDataSource(data)
columns = [TableColumn(field=attr, title=attr) for attr in data.columns]
data_table = DataTable(source=source, columns=columns, width=950, height=500)
show(data_table)