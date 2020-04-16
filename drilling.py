from bokeh.plotting import figure
from bokeh.layouts import row
from flask import request, flash
from pwptemp.wellpath import get
import pwptemp.drilling as ptd


def define_drill_plot():
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
    dt_tdsi = request.args.get("dt_tdsi")
    dt_ta = request.args.get("dt_ta")
    dt_tr = request.args.get("dt_tr")
    dt_tcsg = request.args.get("dt_tcsg")
    dt_tfm = request.args.get("dt_tfm")
    dt_tsr = request.args.get("dt_tsr")

    # TUBULAR
    n_casings = request.args.get("n_casings")
    dro = request.args.get("dro")
    dri = request.args.get("dri")
    ddo = request.args.get("ddo")
    ddi = request.args.get("ddi")

    # OPERATIONAL PARAMETERS
    tin = request.args.get("tin")
    q = request.args.get("q")
    rpm = request.args.get("rpm")
    tbit = request.args.get("tbit")
    wob = request.args.get("wob")
    rop = request.args.get("rop")
    an = request.args.get("an")

    # DENSITIES
    rhof = request.args.get("rhof")
    rhod = request.args.get("rhod")
    rhoc = request.args.get("rhoc")
    rhor = request.args.get("rhor")
    rhofm = request.args.get("rhofm")
    rhow = request.args.get("rhow")
    rhocem = request.args.get("rhocem")

    wtg = request.args.get("wtg")
    gt = request.args.get("gt")

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
        dt_tdsi = True
        dt_ta = False
        dt_tr = False
        dt_tcsg = False
        dt_tfm = True
        dt_tsr = False
        n_casings = 0

        # TUBULAR
        casings_list = []
        dro = 21
        dri = 17.716
        ddo = 4.5
        ddi = 4

        # OPERATIONAL PARAMETERS
        tin = 20
        q = 794.933
        rpm = 100
        tbit = 1.35
        wob = 22.41
        rop = 14.4
        an = 3100

        # DENSITIES
        rhof = 1.198
        rhod = 7.6
        rhoc = 7.8
        rhor = 7.8
        rhofm = 2.245
        rhow = 1.029
        rhocem = 2.7

        wtg = -0.005
        gt = 0.0238

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
        dt_tdsi = bool(dt_tdsi)
        dt_ta = bool(dt_ta)
        dt_tr = bool(dt_tr)
        dt_tcsg = bool(dt_tcsg)
        dt_tfm = bool(dt_tfm)
        dt_tsr = bool(dt_tsr)
        n_casings = int(n_casings)

        # TUBULAR
        casings_list = []
        for i in range(1, n_casings + 1):
            csg_dict = {"od": float(request.args.get("od" + str(i))), "id": float(request.args.get("id" + str(i))),
                        "depth": float(request.args.get("depth" + str(i)))}
            casings_list.append(csg_dict)
        dro = float(dro)
        dri = float(dri)
        ddo = float(ddo)
        ddi = float(ddi)

        # OPERATIONAL PARAMETERS
        tin = float(tin)
        q = float(q)
        rpm = float(rpm)
        tbit = float(tbit)
        wob = float(wob)
        rop = float(rop)
        an = float(an)

        # DENSITIES
        rhof = float(rhof)
        rhod = float(rhod)
        rhoc = float(rhoc)
        rhor = float(rhor)
        rhofm = float(rhofm)
        rhow = float(rhow)
        rhocem = float(rhocem)

        wtg = float(wtg)
        gt = float(gt)

    inputs = {'time': time, 'depth': depth, 'wd': wd, 'well_profile': well_profile, 'kop': kop, 'eob': eob,
              'build_angle': build_angle, 'kop2': kop2, 'eob2': eob2, 'sod': sod, 'eod': eod, 'plot_type': plot_type,
              'n_casings': n_casings}

    # Others parameters: the ones which should be used for the attribute 'change_inputs'
    others = {'wd': wd, 'tin': tin, 'q': q, 'rpm': rpm, 'tbit': tbit, 'wob': wob, 'rop': rop, 'an': an, 'rhof': rhof,
              'rhod': rhod, 'rhoc': rhoc, 'rhor': rhor, 'rhofm': rhofm, 'rhow': rhow, 'rhocem': rhocem, 'dro': dro,
              'dri': dri, 'ddo': ddo, 'ddi': ddi, 'wtg': wtg, 'gt': gt}

    inputs.update(others)  # Merge 'others' into the 'inputs' dictionary

    error_raised = error_messages(inputs)  # Checking process for warning messages depending on the inputs

    if error_raised == 0:
        if plot_type != 5:
            temp = ptd.temp(time, mdt=depth, casings=casings_list, profile=well_profile, change_input=others,
                            build_angle=build_angle, kop=kop, eob=eob, kop2=kop2, eob2=eob2, sod=sod, eod=eod)

        if plot_type == 1:
            fig1 = create_figure1(temp)
        if plot_type == 4:
            fig1 = create_figure4(temp.behavior())
        if plot_type == 5:
            temp = ptd.temp(time, mdt=depth, log=True, profile=well_profile, change_input=others,
                              build_angle=build_angle, kop=kop, eob=eob, kop2=kop2, eob2=eob2, sod=sod, eod=eod)
            fig1 = create_figure5(temp, tdsi=dt_tdsi, ta=dt_ta, tr=dt_tr, tcsg=dt_tcsg, tfm=dt_tfm, tsr=dt_tsr)

        wellpath = get(depth, profile=well_profile, build_angle=build_angle, kop=kop, eob=eob, kop2=kop2,
                       eob2=eob2, sod=sod, eod=eod)
        fig2 = plot_wellpath(wellpath)

        p = row(fig2, fig1)

    else:
        p = figure(sizing_mode='stretch_both')

    return p, inputs


def plot_wellpath(wellpath):
    p = figure(sizing_mode='stretch_both')
    p.line(wellpath.north, wellpath.tvd, line_color='blue')
    p.xaxis.axis_label = 'North, m'
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
    p.yaxis.axis_label = 'MD, m'
    p.title.text = 'Temperature Profile at %1.1f hours' % temp.time
    p.y_range.flipped = True  # reversing y axis
    p.toolbar.active_drag = None  # disable drag by default
    return p


def create_figure4(behavior):
    p = figure(sizing_mode='stretch_both')
    time = int(behavior.finaltime)
    p.line(range(time), behavior.tbot, line_color='blue', legend_label='Bottom')  # Temp. outlet vs Time
    p.line(range(time), behavior.tout, line_color='red', legend_label='Outlet (Annular)')  # Temp. inside Annulus vs Time
    p.line(range(time), [behavior.tfm[-1]] * len(behavior.tbot), line_color='black', legend_label='Formation')  # Formation Temp. vs Time
    p.xaxis.axis_label = 'Time, h'
    p.yaxis.axis_label = 'Temperature, °C'
    p.title.text = 'Temperature behavior (%1.1f hours)' % behavior.finaltime
    p.toolbar.active_drag = None  # disable drag by default
    return p


def create_figure5(temp, tdsi=True, ta=False, tr=False, tcsg=False, tfm=True, tsr=False):
    values = temp.temp_log
    times = [x for x in temp.time_log]

    if temp.time > 5:
        first_quarter = int(len(values) / 3)
        second_quarter = int(len(values) / 3) * 2
        values = [values[0], values[first_quarter], values[second_quarter], values[-1]]
        times = [times[0], times[first_quarter], times[second_quarter], times[-1]]

    p = figure(sizing_mode='stretch_both')
    md = temp.md
    riser = temp.riser
    csg = temp.csgs_reach
    base = ['red', 'blue', 'green', 'orange', 'olive', 'powderblue', 'salmon', 'goldenrod', 'chocolate', 'cadetblue']
    color = []
    for i in range(2):
        color += base
    if tfm:
        p.line(temp.tfm, md, line_color='black', legend_label='Formation - Initial')  # Temp. due to gradient vs Depth
    if len(values) > len(color):
        color = color * round((len(values) / len(color)))
    for x in range(len(values)):
        # Plotting Temperature PROFILE
        if tdsi:
            p.line(values[x].tdsi, md, line_color=color[x], legend_label='Fluid in Drill String at %1.1f hours' % times[x])
        if ta:
            p.line(values[x].ta, md, line_color=color[x+len(values)], legend_label='Fluid in Annulus at %1.1f hours' % times[x])
        if riser > 0 and tr:
            tr = [i for i in values[x].tr if i]
            p.line(tr, md, line_color=color[x+len(values)*2], legend_label='Riser at %1.1f hours' % times[x])
        if csg > 0 and tcsg:
            tcsg_list = [i for i in values[x].tcsg if i]
            p.line(tcsg_list, md, line_color=color[x+len(values)*2], legend_label='Casing at %1.1f hours' % times[x])
        if tsr:
            # Temp. due to gradient vs Depth
            p.line(values[x].tsr, md, line_color=color[x], legend_label='Surrounding Space')
    p.xaxis.axis_label = 'Temperature, °C'
    p.yaxis.axis_label = 'Depth, m'
    p.title.text = 'Temperature Profiles'
    p.legend.click_policy = "hide"
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

    return error_raised

