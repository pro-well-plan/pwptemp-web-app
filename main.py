from flask import Flask, render_template, request, Response
import pwptemp.drilling as ptd
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/plot.png", methods=["GET", "POST"])
def plot_png():
    if request.method == "POST":
        time = int(request.form.get("time"))
        depth = int(request.form.get("depth"))
        wd = int(request.form.get("wd"))
        well_profile = str(request.form.get("well_profile"))
        kop = int(request.form.get("kop"))
        eob = int(request.form.get("eob"))
        build_angle = int(request.form.get("build_angle"))
        kop2 = int(request.form.get("kop2"))
        eob2 = int(request.form.get("eob2"))
        sod = int(request.form.get("sod"))
        eod = int(request.form.get("eod"))

        temp = ptd.temp(time, mdt=depth, profile=well_profile, change_input={'wd': wd}, build_angle=build_angle,
                     kop=kop, eob=eob, kop2=kop2, eob2=eob2, sod=sod, eod=eod)

        plot_type = int(request.form.get("plot_type"))
        plot_md = int(request.form.get("plot_md"))

    if plot_type == 1:
        fig = create_figure1(temp)
    if plot_type == 2:
        fig = create_figure2(temp, plot_md)
    if plot_type == 3:
        fig = create_figure3(temp)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def create_figure1(temp, sr=False):
    fig = Figure()
    ax = fig.add_subplot(1, 1, 1)
    md = temp.md
    riser = temp.riser
    csg = temp.csgs_reach
    ax.plot(temp.tdsi, md, c='r', label='Fluid in Drill String')  # Temp. inside Drillpipe vs Depth
    ax.plot(temp.ta, md, 'b', label='Fluid in Annulus')
    if riser > 0:
        ax.plot(temp.tr, md, 'g', label='Riser')  # Temp. due to gradient vs Depth
    if csg > 0:
        ax.plot(temp.tcsg, md, 'c', label='Casing')  # Temp. due to gradient vs Depth
    ax.plot(temp.tfm, md, color='k', label='Formation')  # Temp. due to gradient vs Depth
    if sr:
        # Temp. due to gradient vs Depth
        ax.plot(temp.tsr, md, c='0.6', ls='-', marker='', label='Surrounding Space')
    ax.set_xlabel('Temperature, °C')
    ax.set_ylabel('Depth, m')
    title = 'Temperature Profile at %1.1f hours' % temp.time
    ax.set_title(title)
    ax.invert_yaxis()  # reversing y axis
    ax.legend()  # applying the legend
    return fig


def create_figure2(temp, md):
    fig = Figure()
    ax = fig.add_subplot(1, 1, 1)
    effect = temp.effect(md_length=md)
    values = [effect.t2, abs(effect.cc), effect.hs, effect.t1]
    bars = ['Tf: %1.2f°C' % effect.t2, 'Convection and Conduction: %1.2f°C' % effect.cc, 'Heat Source Term: %1.2f°C'
            % effect.hs, 'To: %1.2f°C' % effect.t1]
    position = range(4)
    ax.barh(position, values, color=['blue', 'red', 'green', 'blue'])
    if effect.t1 > effect.t2:
        ax.barh(0, abs(effect.cc + effect.hs), color='red', left=effect.t2)
        ax.text(effect.t2, 0, '%1.2f°C' % (effect.cc + effect.hs))
    else:
        ax.barh(0, abs(effect.cc + effect.hs), color='green', left=effect.t1)
        ax.text(effect.t1, 0, '%1.2f°C' % (effect.cc + effect.hs))
    ax.set_yticks(position, ['Tf', 'CC', 'HS', 'To'])
    ax.set_title('Temperature contribution of main factors at %1.1fh - %1.1fm' % (effect.time, effect.length),
              fontweight='bold')
    for i, v in enumerate(values):
        ax.text(v / 8, i, bars[i])
    ax.set_xlabel('Temperature, °C')
    return fig


def create_figure3(temp):
    fig = Figure()
    ax = fig.add_subplot(1, 1, 1)
    effect = temp.well().effect()
    labels = ['pipe rotation in Qp', 'friction in Qp', 'pipe rotation in Qa', 'friction in Qa']
    effects = [effect.ds_rot1, effect.fric1, effect.ds_rot2, effect.fric2]
    ax.pie(effects, startangle=90)
    ax.legend(loc=0, labels=['%s, %1.2f %%' % (l, s) for l, s in zip(labels, effects)])
    title = 'Effect of factors in heat source terms. Qp/Qa = %1.2f' % effect.hsr
    ax.set_title(title)
    return fig

if __name__ == "__main__":
    app.run(debug=True)

