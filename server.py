import io

from flask import Flask, Response, render_template, session, request
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
# from matplotlib.figure import Figure

from Graph import create_plot, create_temp_time_plot
import pwptemp
from pwptemp.main import temp_time, stab_time
deltaz =50
target_depth = 4000
tdata = pwptemp.input.tdict(deltaz)
depths = pwptemp.wellpath.get(target_depth, deltaz)
well = pwptemp.input.set_well(tdata, depths)

app = Flask(__name__)
app.secret_key = b'\xba\x1d\x88\x98\xa0\x06\xce\x98g\x1d\xd4s\x81\x92@\xc6'

@app.route('/', methods=['GET', 'POST'])
def show_temp_plot():
    """
    Renders template which calls for figures
    """
    if request.method == 'POST':
            steps=request.form['timesteps']
            session['timesteps']=[float(n) for n in steps.split(',')]
    if 'timesteps' not in session:
        session['timesteps'] = [6]
    if 'show_variables' not in session:
        session['show_variables'] = True
    return render_template('plot.html', timesteps = session['timesteps'], show_variables = session['show_variables'], variables=tdata)

@app.route('/plot.png')
def depth_profile():
    """
    Creates figure and returns to template
    """
    return return_figure(plot_depth_profile())


@app.route('/stab_plot.png')
def time_profile():
    """
    Creates the temperature vs time plot
    """
    
    return return_figure(plot_time_profile())

def plot_time_profile():
    well= create_default_well()
    s_t = stab_time(well)
    fig = plt.figure(dpi=150)
    axis=fig.add_subplot(1,1,1)

    create_temp_time_plot(axis,s_t)
    axis.set_ylim(axis.get_ylim()[::-1])  # reversing y axis
    axis.legend()
    return fig


def plot_depth_profile():
    """
    Loads dataset and create Matplotlib figure using create_ax from Graph library
    """
    well= create_default_well()
    res = []
    for time in session['timesteps']:
        temp_distribution = pwptemp.main.temp_time(time, well)
        res.append(temp_distribution)

    fig = plt.figure(dpi=150)
    axis=fig.add_subplot(1,1,1)

    for temp_dist in res:
        create_plot(axis,temp_dist,well)
    axis.set_ylim(axis.get_ylim()[::-1])  # reversing y axis
    axis.legend()
    return fig

def create_default_well():
    """
    Initiate and return well instance from tdata and dephts
    """
    return pwptemp.input.set_well(tdata, depths)


def return_figure(fig):
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
