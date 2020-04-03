from flask import Flask, render_template, request, flash
import pwptemp.drilling as ptd
from drilling import *
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


@app.route("/production")
def production():
    return render_template("production.html")


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
                           rpm=inputs['rpm'], tbit=inputs['tbit'], wob=inputs['wob'], rop=inputs['rop'],
                           an=inputs['an'], rhof=inputs['rhof'], rhod=inputs['rhod'], rhoc=inputs['rhoc'],
                           rhor=inputs['rhor'], rhofm=inputs['rhofm'], rhow=inputs['rhow'], rhocem=inputs['rhocem'],
                           n_casings=inputs['n_casings'], dro=inputs['dro'], dri=inputs['dri'],
                           ddo=inputs['ddo'], ddi=inputs['ddi'], wtg=inputs['wtg'], gt=inputs['gt'])

    return encode_utf8(html)


def plot():
    p, inputs = define_plot()
    return p, inputs


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


if __name__ == "__main__":
    app.run(debug=True)

