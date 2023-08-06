# for nice interactive plots a good library is Bokeh

from bokeh.plotting import figure, show
from bokeh.layouts import gridplot, column, row
from bokeh import palettes
from bokeh.io import output_notebook
from bokeh.tile_providers import get_provider
from bokeh.models import ColorBar, LinearColorMapper, ColumnDataSource, HoverTool
from bokeh.resources import INLINE
output_notebook(resources=INLINE)