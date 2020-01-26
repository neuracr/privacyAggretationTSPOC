from math import exp
import logging

from bokeh.layouts import layout
from bokeh.models import Button
from bokeh.plotting import figure, curdoc
from bokeh.models.glyphs import VBar
from bokeh.models import (ColumnDataSource, TextInput, Slider, Div, Paragraph,
                          Whisker)
from bokeh.models import Toggle
from os.path import dirname, join
from bokeh.driving import linear


from main import experiment_basic


# Fixed variables:
number_participants = [10, 100, 1000, 10000]

# Widget variables (parameters for the simulation):
eps = TextInput(title="ε", value=str(0.1))
eps_slider = Slider(title="ε", value=float(eps.value), start=0, end=2,
                    step=0.1)
small_delta = TextInput(title="δ", value=str(0.01))
small_delta_slider = Slider(title="δ", value=float(small_delta.value), start=0,
                            end=2, step=0.01)
big_delta = TextInput(title="Δ", value=str(87))
big_delta_slider = Slider(title="Δ", value=float(big_delta.value), start=1,
                          end=2000, step=1)
gamma = TextInput(title="γ", value=str(0.2))
gamma_slider = Slider(title="γ", value=float(gamma.value), start=0, end=1,
                      step=0.1)

# result of the standard deviation of the symmetric geometric law for the noise
geo_text = Paragraph(text="")

# Toggle the simulation on/off
enable_1exp_btn = Toggle(active=True, label="Enable simulation")
enable_refine_btn = Toggle(active=False, label="Enable error stat refining")
err_percent_btn = Toggle(active=False, label="Computes all errors in percent")
redo_1exp_btn = Button(label="Redo experiment")

# tracks if one of the parameter changed to know if we start the stats from
# 0 again
has_param_changed = True

source_1exp = ColumnDataSource(data=dict(n=[], error=[]))

p_1exp = figure(plot_height=350, title="1 time error", x_axis_type="log",
                y_range=[0, 100], tools="ypan, ywheel_pan, ywheel_zoom",
                y_axis_label="error", x_axis_label="nb participants")
glyph = VBar(x='n', top='error', bottom=0.1, width="n", hatch_scale=None)
p_1exp.add_glyph(source_1exp, glyph)
p_1exp.y_range.start = 0
p_1exp.x_range.range_padding = 0.1
p_1exp.xaxis.major_label_orientation = 1
p_1exp.xgrid.grid_line_color = None


def modular_abs(x, y, p):
    return(min((x-y) % p, (y-x) % p))


def update_1exp():
    sanitize_params()
    eps_val = float(eps.value)
    small_delta_val = float(small_delta.value)
    big_delta_val = float(big_delta.value)
    gamma_val = float(gamma.value)

    # https://www.wolframalpha.com/input/?i=%E2%88%91a%5E%28-i%29*i%5E2
    alpha = exp(eps_val/big_delta_val)
    geo_sigma = (2*alpha/((alpha-1)**2))**0.5
    geo_text.text = ('Standard deviation of the added noise σ(Geom(α)) = %d'
                     % (geo_sigma))

    if not enable_1exp_btn.active:
        return

    new_data = dict(n=[], error=[])
    for n in number_participants:
        res, real, p = experiment_basic(n, 1337, eps_val, small_delta_val,
                                        big_delta_val, gamma_val)

        new_data['n'].append(n)
        err = modular_abs(real, res, p)
        if err_percent_btn.active:
            err = err/real*100
        new_data['error'].append(err)
        print(res, real, p, modular_abs(real, res, p), err)
    source_1exp.data = new_data


def on_textinput_change():
    global has_param_changed

    # Disable simulation to prevent many computations
    has_param_changed = True
    enable_1exp_btn.active = False
    enable_refine_btn.active = False
    eps_slider.value = float(eps.value)
    small_delta_slider.value = float(small_delta.value)
    big_delta_slider.value = float(big_delta.value)
    gamma_slider.value = max(float(gamma.value), 0.001)


def on_slider_change():
    global has_param_changed

    # Disable simulation to prevent many computations
    has_param_changed = True
    enable_1exp_btn.active = False
    enable_refine_btn.active = False
    eps.value = str(eps_slider.value)
    small_delta.value = str(small_delta_slider.value)
    big_delta.value = str(big_delta_slider.value)
    gamma.value = str(max(gamma_slider.value, 0.001))


# data for the empirical study of the error
source_stat = ColumnDataSource(data=dict(n_participants=[], n_iterations=[],
                               mean_error=[], std_deviation=[], upper=[],
                               lower=[]))

p_error_stat = figure(plot_height=350,
                      title="empirical mean, std deviation error",
                      x_axis_type="log",
                      y_range=[0, 100],
                      tools="ypan, ywheel_pan, ywheel_zoom",
                      y_axis_label="error",
                      x_axis_label="nb participants")

# mean error bar
glyph = VBar(x='n_participants', top='mean_error', bottom=0.1,
             width="n_participants", hatch_scale=None)
p_error_stat.add_glyph(source_stat, glyph)
p_error_stat.y_range.start = 0
p_error_stat.x_range.range_padding = 0.1
p_error_stat.xaxis.major_label_orientation = 1
p_error_stat.xgrid.grid_line_color = None

# overlay for the standard deviation
p_error_stat.add_layout(
    Whisker(source=source_stat, base="n_participants", upper="upper",
            lower="lower", level="overlay")
)


@linear()
def refine_stat(step):
    """Refine the experimental computation of the mean and deviation of
       the error"""
    sanitize_params()
    eps_val = float(eps.value)
    small_delta_val = float(small_delta.value)
    big_delta_val = float(big_delta.value)
    gamma_val = float(gamma.value)

    if not enable_refine_btn.active:
        return

    global has_param_changed
    # if the parameters of the simulation have changed, we need to recompute
    # everything from scratch
    if has_param_changed:
        n = len(number_participants)
        source_stat.data = dict(n_participants=number_participants,
                                n_iterations=[0]*n,
                                mean_error=[0]*n,
                                std_deviation=[0]*n,
                                upper=[0]*n,
                                lower=[0]*n)
        has_param_changed = False

    new_data = dict(n_participants=[], n_iterations=[], mean_error=[],
                    std_deviation=[], upper=[], lower=[])

    for i in range(len(number_participants)):
        res, real, p = experiment_basic(number_participants[i], 1337, eps_val,
                                        small_delta_val, big_delta_val,
                                        gamma_val)
        err = modular_abs(real, res, p)
        if err_percent_btn.active:
            err = err/real*100

        current_iteration_nb = source_stat.data['n_iterations'][i]+1
        new_data['n_participants'] += [number_participants[i]]
        new_data['mean_error'] += [(source_stat.data['mean_error'][i])
                                   * (current_iteration_nb-1)
                                   / (current_iteration_nb)
                                   + err / current_iteration_nb]
        new_data['std_deviation'] += [(source_stat.data['std_deviation'][i]**2
                                      * (current_iteration_nb-1)
                                      / current_iteration_nb
                                      + err**2 / current_iteration_nb)**0.5]
        new_data['upper'] += [new_data['mean_error'][-1]
                              + new_data['std_deviation'][-1]]
        new_data['lower'] += [new_data['mean_error'][-1]
                              - new_data['std_deviation'][-1]]
        new_data['n_iterations'] += [current_iteration_nb]
    source_stat.data = new_data
    for x in source_stat.data.keys():
        print(x, str(source_stat.data[x]))


def on_err_percent_btn_changed(attr, old, new):
    global has_param_changed
    has_param_changed = True


def sanitize_params():
    eps.value = str(float(eps.value))
    eps_slider.value = float(eps_slider.value)
    small_delta.value = str(float(small_delta.value))
    small_delta_slider.value = float(small_delta_slider.value)
    big_delta.value = str(int(float(big_delta.value)))
    big_delta_slider.value = int(big_delta_slider.value)
    gamma.value = str(float(gamma.value))
    gamma_slider.value = float(gamma_slider.value)


desc = Div(text=open(join(dirname(__file__), "error_plot.html")).read(),
           sizing_mode="stretch_width")

lay = layout([
    [desc],
    [eps, eps_slider],
    [small_delta, small_delta_slider],
    [big_delta, big_delta_slider],
    [gamma, gamma_slider],
    [geo_text],
    [err_percent_btn, enable_1exp_btn, enable_refine_btn],
    [p_1exp, p_error_stat],
    [redo_1exp_btn]
])

controls = [eps, small_delta, big_delta, gamma]
for control in controls:
    control.on_change('value', lambda attr, old, new: update_1exp())

err_percent_btn.on_change('active', on_err_percent_btn_changed)

redo_1exp_btn.on_click(update_1exp)

enable_1exp_btn.on_change('active', lambda attr, old, new: update_1exp())
sliders = [eps_slider, small_delta_slider, big_delta_slider, gamma_slider]
for slider in sliders:
    slider.on_change('value', lambda attr, old, new: on_slider_change())

textinputs = [eps, small_delta, big_delta, gamma]
for ti in textinputs:
    ti.on_change('value', lambda attr, old, new: on_textinput_change())

# put the button and plot in a layout and add to the document
curdoc().add_root(lay)
curdoc().title = "Empirical error"
update_1exp()
curdoc().add_periodic_callback(refine_stat, 500)
logging.basicConfig(level=logging.DEBUG)
