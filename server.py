import io

from flask import Flask, Response, render_template, session, request
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
# from matplotlib.figure import Figure


import pwptemp
from pwptemp.main import temp_time
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
    Renders template which calls for figure
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
    fig = plot_depth_profile()
    return return_figure(fig)


@app.route('/stab_plot.png')
def time_profile():
    """
    Creates the temperature vs time plot
    """
    well, md, tvd, deltaz, zstep = create_default_well()
    
    Tdsi, Ta, Tr, Tcsg, Tsr, Tfm, time = pwptemp.main.temp_time(5, well, tvd, deltaz, zstep)
    
    finaltime, Tbot, Tout = stab_time(well, tvd, deltaz, zstep)

    fig = plt.figure(dpi=150)
    axis=fig.add_subplot(1,1,1)
    
    create_temp_time_plot(axis,finaltime,Tbot,Tout,Tfm)
    return return_figure(fig)

def plot_depth_profile():
    """
    Loads dataset and create Matplotlib figure using create_ax from Graph library
    """
    well, md, tvd, deltaz, zstep = create_default_well()
    res = []
    for time in session['timesteps']:
        temp_distribution = pwptemp.main.temp_time(circulation_time, well)
        res.append(temp_distribution)

    fig = plt.figure(dpi=150)
    axis=fig.add_subplot(1,1,1)

    for step in res:
        create_plot(axis, step,well)
    axis.set_ylim(axis.get_ylim()[::-1])  # reversing y axis
    axis.legend()
    return fig

def create_default_well():
    # tdata=temp_dict 
    well = pwptemp.input.set_well(tdata, depths)

    return well 

def return_figure(fig):
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
