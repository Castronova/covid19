import datetime
from os.path import dirname, join

import pandas as pd
from scipy.signal import savgol_filter

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, DataRange1d, Select
from bokeh.palettes import Blues4
from bokeh.plotting import figure

mode = 'cumulative'
style= 'line'
agg = 'daily'

plot = figure(x_axis_type="datetime",
              plot_width=800,
              tools="", toolbar_location=None)
plot.title.text = "Covid Deaths"


df = pd.read_csv('dat/covid-deaths.tsv',
                 delimiter='\t')

state = 'Massachusetts'
states = df.columns[1:]
state_select = Select(value=state,
                      title='State',
                      options=sorted(states))
mode_select = Select(value='Cumulative',
                     title='Mode',
                     options=['Cumulative',
                              'Instantaneous',
                              'Rate of Change'])
agg_select = Select(value='Cumulative',
                    title='Aggregation',
                    options=['Daily',
                             'Weekly',
                             '7-Day Ave'])
style_select = Select(value='Line',
                        title='Style',
                        options=['Line',
                                 'Bar'])
# percent per capita option? 


dates = pd.to_datetime(df.date, format='%Y%m%d')
source = ColumnDataSource(data=dict(x=dates,
                                    y=df[state]))

line = plot.line('x', 'y',
                 source=source,
                 line_width=3,
                 line_alpha=0.6)
vbar = plot.vbar(x='x', top='y', width=0.2,
                 source=source)
vbar.visible = False


# fixed attributes
plot.xaxis.axis_label = None
plot.yaxis.axis_label = "Death Count"
plot.axis.axis_label_text_font_style = "bold"
plot.x_range = DataRange1d(range_padding=0.0)
plot.grid.grid_line_alpha = 0.3

def update_plot(attrname, old, new):
    state = state_select.value
    plot.title.text = f"COVID Deaths for {state}"
    source.data = dict(x=dates, y=df[state])
    update_style(None, None, style_select.value)
    update_mode(None, None, mode_select.value)
    update_agg(None, None, agg_select.value)

def update_style(attrname, old, new):
    style = new.lower()
    if style == 'line':
        line.visible = True
        vbar.visible = False
    if style == 'bar':
        line.visible = False
        vbar.visible = True

def update_mode(attrname, old, new):
    agg = new.lower()
    state = state_select.value
    if agg == 'cumulative':
        source.data = dict(x=dates, y=df[state])
    if agg == 'instantaneous':
        source.data = dict(x=dates,
                           y=df[state].diff())

def update_agg(attrname, old, new):
    # create new dataframe from current x,y data
    # then perform date agg
    df = pd.DataFrame(source.data)
    df = df.set_index('x')

    if new == 'weekly':
        df = df.groupby(pd.TimeGrouper('W')).sum().dropna()
    if new == 'daily':
        df = df.groupby(pd.TimeGrouper('D')).sum().dropna()

    source.data = dict(x=df.index, y=df.y)

    print('Update Agg not implemented')


#    src = get_dataset(df, cities[city]['airport'], distribution_select.value)
#    source.data.update(src.data)

state_select.on_change('value', update_plot)
style_select.on_change('value', update_style)
mode_select.on_change('value', update_mode)
controls = column(state_select,
                  mode_select,
                  style_select,
                  agg_select)
curdoc().add_root(row(plot, controls))
curdoc().title = "Covid Deaths"


