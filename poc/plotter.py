
from random import random

from bokeh.layouts import column, layout
from bokeh.models import Button
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc

from bokeh.models import ColumnDataSource, FactorRange, Slider, Div
from bokeh.transform import factor_cmap
from os.path import dirname, join


from main import experiment_basic


# Fixed variables:
number_participants = [10, 100, 1000, 10000]

# Widget variables:
eps = Slider(title="ε", value=0.1, start=0, end=2, step=0.1)
small_delta = Slider(title="δ", value=0.1, start=0, end=2, step=0.01)
big_delta = Slider(title="Δ", value=2000, start=0, end=10000, step=10)
gamma = Slider(title="γ", value=0.1, start=0, end=2, step=0.01)

palette = ["#c9d9d3", "#718dbf", "#e84d60"]

source = ColumnDataSource(data=dict(n=[1], mean_error=[1], std_deviation=[1]))

p = figure(plot_height=350, title="Error", x_axis_type="log",
           toolbar_location=None, tools="")

r = p.vbar(x='n', top='mean_error', width=6, source=source, line_color="red")

p.y_range.start = 0
p.x_range.range_padding = 0.1
p.xaxis.major_label_orientation = 1
p.xgrid.grid_line_color = None

# add a text renderer to our plot (no data yet)
# r = p.text(x=[], y=[], text=[], text_color=[], text_font_size="20pt",
#            text_baseline="middle", text_align="center")

ds = r.data_source


def generate_stat(n):
    eps_val = eps.value
    small_delta_val = small_delta.value
    big_delta_val = big_delta.value
    gamma_val = gamma.value

    return experiment_basic(n, 1337, eps_val, small_delta_val,
                            big_delta_val, gamma_val)


# create a callback that will add a number in a random location
def update():

    # BEST PRACTICE --- update .data in one step with a new dict
    new_data = dict(n=[], mean_error=[], std_deviation=[])
    for n in number_participants:
        res, real = generate_stat(n)
        new_data['n'].append(n)
        new_data['mean_error'].append(real-res)
        new_data['std_deviation'].append(real-res)
        print(res, real)
    ds.data = new_data


desc = Div(text=open(join(dirname(__file__), "error_plot.html")).read(), sizing_mode="stretch_width")

l = layout([
    [desc],
    [eps],
    [small_delta],
    [big_delta],
    [gamma],
    [p]
])

controls = [eps, small_delta, big_delta, gamma]
for control in controls:
    control.on_change('value', lambda attr, old, new: update())

# put the button and plot in a layout and add to the document
curdoc().add_root(l)
curdoc().title = "Empirical error"
update()
