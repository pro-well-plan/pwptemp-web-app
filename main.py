from flask import Flask, render_template, request, flash
import pwptemp.drilling as ptd
from bokeh.plotting import figure, output_file
from bokeh.layouts import row
from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
from pwptemp.wellpath import get

app = Flask(__name__)
app.secret_key = 'random secret'


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/contributors")
def contributors():
    return render_template("contributors.html")


@app.route("/drilling")
def drilling():
    p, inputs = plot()

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # Embed plot into HTML via Flask Render
    script, div = components(p)
    html = render_template('drilling.html', plot_script=script, plot_div=div, js_resources=js_resources,
                           css_resources=css_resources, time=inputs['time'], depth=inputs['depth'], wd=inputs['wd'],
                           kop=inputs['kop'], eob=inputs['eob'], build_angle=inputs['build_angle'], kop2=inputs['kop2'],
                           eob2=inputs['eob2'], sod=inputs['sod'], eod=inputs['eod'], tin=inputs['tin'], q=inputs['q'],
                           rpm=inputs['rpm'], t=inputs['t'], tbit=inputs['tbit'], wob=inputs['wob'], rop=inputs['rop'],
                           an=inputs['an'], rhol=inputs['rhol'], rhod=inputs['rhod'], rhoc=inputs['rhoc'],
                           rhor=inputs['rhor'], rhofm=inputs['rhofm'], rhow=inputs['rhow'], rhocem=inputs['rhocem'],
                           plot_md=inputs['plot_md'], deltat=inputs['deltat'], n_casings=inputs['n_casings'])

    return encode_utf8(html)


def plot():
    time = request.args.get("time")
    depth = request.args.get("depth")
    wd = request.args.get("wd")
    well_profile = request.args.get("well_profile")
    kop = request.args.get("kop")
    eob = request.args.get("eob")
    build_angle = request.args.get("build_angle")
    kop2 = request.args.get("kop2")
    eob2 = request.args.get("eob2")
    sod = request.args.get("sod")
    eod = request.args.get("eod")
    plot_type = request.args.get("plot_type")
    plot_md = request.args.get("plot_md")
    deltat = request.args.get("deltat")
    dt_tdsi = request.args.get("dt_tdsi")
    dt_ta = request.args.get("dt_ta")
    dt_tr = request.args.get("dt_tr")
    dt_tcsg = request.args.get("dt_tcsg")
    dt_tfm = request.args.get("dt_tfm")
    dt_tsr = request.args.get("dt_tsr")
    n_casings = request.args.get("n_casings")

    # OPERATIONAL PARAMETERS
    tin = request.args.get("tin")
    q = request.args.get("q")
    rpm = request.args.get("rpm")
    t = request.args.get("t")
    tbit = request.args.get("tbit")
    wob = request.args.get("wob")
    rop = request.args.get("rop")
    an = request.args.get("an")

    # DENSITIES
    rhol = request.args.get("rhol")
    rhod = request.args.get("rhod")
    rhoc = request.args.get("rhoc")
    rhor = request.args.get("rhor")
    rhofm = request.args.get("rhofm")
    rhow = request.args.get("rhow")
    rhocem = request.args.get("rhocem")

    if time is None:
        time = 5
        depth = 3000
        wd = 150
        well_profile = "V"
        kop = 600
        eob = 1500
        build_angle = 40
        kop2 = 1800
        eob2 = 2300
        sod = 2000
        eod = 2600
        plot_type = 1
        plot_md = 1
        deltat = 1
        dt_tdsi = True
        dt_ta = False
        dt_tr = False
        dt_tcsg = False
        dt_tfm = True
        dt_tsr = False
        n_casings = 0
        casings_list = []

        # OPERATIONAL PARAMETERS
        tin = 20
        q = 47.696
        rpm = 100
        t = 2
        tbit = 1.35
        wob = 22.41
        rop = 14.4
        an = 2

        # DENSITIES
        rhol = 1198
        rhod = 7600
        rhoc = 7800
        rhor = 7800
        rhofm = 2245
        rhow = 1029
        rhocem = 2700

    else:
        time = float(time)
        depth = float(depth)
        wd = float(wd)
        well_profile = str(well_profile)
        kop = float(kop)
        eob = float(eob)
        build_angle = int(build_angle)
        kop2 = float(kop2)
        eob2 = float(eob2)
        sod = float(sod)
        eod = float(eod)
        plot_type = int(plot_type)
        plot_md = float(plot_md)
        deltat = float(deltat)
        dt_tdsi = bool(dt_tdsi)
        dt_ta = bool(dt_ta)
        dt_tr = bool(dt_tr)
        dt_tcsg = bool(dt_tcsg)
        dt_tfm = bool(dt_tfm)
        dt_tsr = bool(dt_tsr)
        n_casings = int(n_casings)
        casings_list = []
        for i in range(1, n_casings+1):
            csg_dict = {"od": float(request.args.get("od" + str(i))), "id": float(request.args.get("id" + str(i))),
                        "depth": float(request.args.get("depth" + str(i)))}
            casings_list.append(csg_dict)

            # OPERATIONAL PARAMETERS
        tin = float(tin)
        q = float(q)
        rpm = float(rpm)
        t = float(t)
        tbit = float(tbit)
        wob = float(wob)
        rop = float(rop)
        an = float(an)

        # DENSITIES
        rhol = float(rhol)
        rhod = float(rhod)
        rhoc = float(rhoc)
        rhor = float(rhor)
        rhofm = float(rhofm)
        rhow = float(rhow)
        rhocem = float(rhocem)

    inputs = {'time':time, 'depth':depth, 'wd':wd, 'well_profile':well_profile, 'kop':kop, 'eob':eob,
              'build_angle':build_angle, 'kop2':kop2, 'eob2':eob2, 'sod':sod, 'eod':eod, 'plot_type':plot_type,
              'plot_md':plot_md, 'deltat':deltat, 'n_casings':n_casings}

    # Others parameters: the ones which should be used for the attribute 'change_inputs'
    others = {'wd':wd, 'tin':tin, 'q':q, 'rpm':rpm, 't':t, 'tbit':tbit, 'wob':wob, 'rop':rop, 'an':an, 'rhol':rhol,
              'rhod':rhod, 'rhoc':rhoc, 'rhor':rhor, 'rhofm':rhofm, 'rhow':rhow, 'rhocem':rhocem}

    inputs.update(others)  # Merge 'others' into the 'inputs' dictionary

    error_raised = error_messages(inputs)  # Checking process for warning messages depending on the inputs

    if error_raised == 0:
        if plot_type != 5:
            temp = ptd.temp(time, mdt=depth, casings=casings_list, profile=well_profile, change_input=others,
                            build_angle=build_angle, kop=kop, eob=eob, kop2=kop2, eob2=eob2, sod=sod, eod=eod)

        if plot_type == 1:
            fig1 = create_figure1(temp)
        if plot_type == 2:
            fig1 = create_figure2(temp, plot_md)
        if plot_type == 3:
            fig1 = create_figure3(temp)
        if plot_type == 4:
            fig1 = create_figure4(temp.stab())
        if plot_type == 5:
            temps = ptd.temps(time, deltat, mdt=depth, profile=well_profile, change_input=others, build_angle=build_angle,
                              kop=kop, eob=eob, kop2=kop2, eob2=eob2, sod=sod, eod=eod)
            fig1 = create_figure5(temps, tdsi=dt_tdsi, ta=dt_ta, tr=dt_tr, tcsg=dt_tcsg, tfm=dt_tfm, tsr=dt_tsr)

        wellpath = get(depth, profile=well_profile, build_angle=build_angle, kop=kop, eob=eob, kop2=kop2,
                                       eob2=eob2, sod=sod, eod=eod)
        fig2 = plot_wellpath(wellpath)

        p = row(fig2, fig1)

    else:
        p = figure(sizing_mode='stretch_both')

    return p, inputs


def plot_wellpath(wellpath):
    p = figure(sizing_mode='stretch_both')
    p.line(wellpath.hd, wellpath.tvd, line_color='blue')
    p.xaxis.axis_label = 'Horizontal Displacement, m'
    p.yaxis.axis_label = 'TVD, m'
    p.title.text = 'Well Profile'
    p.y_range.flipped = True  # reversing y axis
    p.toolbar.active_drag = None  # disable drag by default
    return p


def create_figure1(temp, sr=False):
    p = figure(sizing_mode='stretch_both')
    md = temp.md
    riser = temp.riser
    tr = [i for i in temp.tr if i]
    csg = temp.csgs_reach
    tcsg = [i for i in temp.tcsg if i]
    p.line(temp.tdsi, md, line_color='red', legend_label='Fluid in Drill String')  # Temp. inside Drillpipe vs Depth
    p.line(temp.ta, md, line_color='blue', legend_label='Fluid in Annulus')
    if riser > 0:
        p.line(tr, md, line_color='green', legend_label='Riser')  # Temp. due to gradient vs Depth
    if csg > 0:
        p.line(tcsg, md, line_color='orange', legend_label='Casing')  # Temp. due to gradient vs Depth
    p.line(temp.tfm, md, line_color='darkred', legend_label='Formation')  # Temp. due to gradient vs Depth
    if sr:
        # Temp. due to gradient vs Depth
        p.line(temp.tsr, md, line_color='salmon', ls='-', marker='', legend_label='Surrounding Space')

    p.xaxis.axis_label = 'Temperature, °C'
    p.yaxis.axis_label = 'Depth, m'
    p.title.text = 'Temperature Profile at %1.1f hours' % temp.time
    p.y_range.flipped = True  # reversing y axis
    p.toolbar.active_drag = None  # disable drag by default
    return p


def create_figure2(temp, plot_md):
    effect = temp.effect(md_length=plot_md)
    values = [effect.cc, effect.hs, effect.cc+effect.hs]
    output_file("bars.html")
    labels = ['Convection and Conduction', 'Heat Source Term', 'Effective Change']
    title = 'Temperature contribution of main factors at %1.1fh - %1.1fm' % (effect.time, effect.length)
    p = figure(x_range=labels, sizing_mode='stretch_both', title=title)
    p.yaxis.axis_label = 'Change in Temperature, °C'
    p.vbar(x=labels, top=values, width=0.5)
    p.toolbar.active_drag = None  # disable drag by default
    return p


def create_figure3(temp):
    hs = temp.effect().hs
    effect = temp.well().effect()
    values = [effect.ds_rot1 * hs, effect.fric1 * hs, effect.ds_rot2 * hs, effect.fric2 * hs]
    output_file("bars.html")
    labels = ['pipe rotation in Qp', 'friction in Qp', 'pipe rotation in Qa', 'friction in Qa']
    title = 'Effect of factors in heat source terms. Qp/Qa = %1.2f' % effect.hsr
    p = figure(x_range=labels, sizing_mode='stretch_both', title=title)
    p.yaxis.axis_label = 'Change in Temperature, °C'
    p.vbar(x=labels, top=values, width=0.5)
    p.toolbar.active_drag = None  # disable drag by default
    return p


def create_figure4(stab_data):
    p = figure(sizing_mode='stretch_both')
    p.line(range(stab_data.finaltime), stab_data.tbot, line_color='blue', legend_label='Bottom')  # Temp. inside Annulus vs Time
    p.line(range(stab_data.finaltime), stab_data.tout, line_color='red', legend_label='Outlet (Annular)')  # Temp. inside Annulus vs Time
    p.line(range(stab_data.finaltime), [stab_data.tfm[-1]] * len(stab_data.tbot), line_color='black', legend_label='Formation')  # Formation Temp. vs Time
    p.xaxis.axis_label = 'Time, h'
    p.yaxis.axis_label = 'Temperature, °C'
    p.title.text = 'Temperature behavior before stabilization (%1.1f hours)' % stab_data.finaltime
    p.toolbar.active_drag = None  # disable drag by default
    return p


def create_figure5(temps, tdsi=True, ta=False, tr=False, tcsg=False, tfm=True, tsr=False):
    p = figure(sizing_mode='stretch_both')
    md = temps.values[0].md
    riser = temps.values[0].riser
    csg = temps.values[0].csgs_reach
    color = ['red', 'blue', 'green', 'orange', 'olive', 'powderblue', 'salmon', 'goldenrod', 'chocolate']
    if tfm:
        p.line(temps.values[0].tfm, md, line_color='black', legend_label='Formation - Initial')  # Temp. due to gradient vs Depth
    if len(temps.values) > len(color):
        color = color * round((len(temps.values) / len(color)))
    for x in range(len(temps.values)):
        # Plotting Temperature PROFILE
        if tdsi:
            p.line(temps.values[x].tdsi, md, line_color=color[x], legend_label='Fluid in Drill String at %1.1f hours' % temps.times[x])
        if ta:
            p.line(temps.values[x].ta, md, line_color=color[x], legend_label='Fluid in Annulus at %1.1f hours' % temps.times[x])
        if riser > 0 and tr:
            tr = [i for i in temps.values[x].tr if i]
            p.line(tr, md, line_color=color[x], legend_label='Riser at %1.1f hours' % temps.times[x])
        if csg > 0 and tcsg:
            tcsg_list = [i for i in temps.values[x].tcsg if i]
            p.line(tcsg_list, md, line_color=color[x], legend_label='Casing at %1.1f hours' % temps.times[x])
        if tsr:
            # Temp. due to gradient vs Depth
            p.line(temps.values[x].tsr, md, line_color=color[x], legen_label='Surrounding Space')
    p.xaxis.axis_label = 'Temperature, °C'
    p.yaxis.axis_label = 'Depth, m'
    p.title.text = 'Temperature Profiles'
    p.y_range.flipped = True  # reversing y axis
    p.toolbar.active_drag = None  # disable drag by default
    return p


def error_messages(inputs):

    error_raised = 0
    if inputs['wd'] > inputs['depth']:
        flash('water depth is higher than the total depth', 'danger')
        error_raised = 1

    if inputs['well_profile'] == "J" or inputs['well_profile'] == "H1":

        if inputs['kop'] > inputs['depth']:
            flash('kop is higher than the total depth', 'danger')
            error_raised = 1

        if inputs['eob'] > inputs['depth']:
            flash('eob is higher than the total depth', 'danger')
            error_raised = 1

        if inputs['eob'] < inputs['kop']:
            flash('eob must be deeper than kop', 'danger')
            error_raised = 1

    if inputs['well_profile'] == "S":

        if inputs['sod'] > inputs['depth']:
            flash('sod is higher than the total depth', 'danger')
            error_raised = 1

        if inputs['eod'] > inputs['depth']:
            flash('eod is higher than the total depth', 'danger')
            error_raised = 1

        if inputs['eod'] < inputs['sod']:
            flash('eob2 must be deeper than kop2', 'danger')
            error_raised = 1

    if inputs['well_profile'] == "H2":

        if inputs['kop2'] > inputs['depth']:
            flash('kop2 is higher than the total depth', 'danger')
            error_raised = 1

        if inputs['eob2'] > inputs['depth']:
            flash('eob2 is higher than the total depth', 'danger')
            error_raised = 1

        if inputs['eob2'] < inputs['kop2']:
            flash('eob2 must be deeper than kop2', 'danger')
            error_raised = 1

    if inputs['plot_type'] == 2:
        if inputs['plot_md'] > 1:
            flash('maximum depth is 1 (bottom)', 'danger')
            error_raised = 1

    if inputs['plot_type'] == 5:
        if inputs['deltat'] > inputs['time']:
            flash('time step must be smaller than the total time', 'danger')
            error_raised = 1

    return error_raised


if __name__ == "__main__":
    app.run(debug=True)

