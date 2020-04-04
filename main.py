from flask import Flask, render_template
from drilling import *
from production import *
from bokeh.embed import components
from bokeh.resources import INLINE

app = Flask(__name__)
app.secret_key = 'random secret'


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/contributors")
def contributors():
    return render_template("contributors.html")


def encode_utf8(u):
    """
    Encode a UTF-8 string to a sequence of bytes.
    :param u: the string to encode
    :return: bytes
    """
    import sys
    if sys.version_info[0] == 2:
        u = u.encode('utf-8')
    return u


@app.route("/production")
def production():
    p, inputs = define_prod_plot()

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # Embed plot into HTML via Flask Render
    script, div = components(p)
    html = render_template('production.html', plot_script=script, plot_div=div, js_resources=js_resources,
                           css_resources=css_resources, time=inputs['time'], depth=inputs['depth'], wd=inputs['wd'],
                           kop=inputs['kop'], eob=inputs['eob'], build_angle=inputs['build_angle'], kop2=inputs['kop2'],
                           eob2=inputs['eob2'], sod=inputs['sod'], eod=inputs['eod'], q=inputs['q'],
                           rhof=inputs['rhof'], rhot=inputs['rhot'], rhoc=inputs['rhoc'],
                           rhor=inputs['rhor'], rhofm=inputs['rhofm'], rhow=inputs['rhow'], rhocem=inputs['rhocem'],
                           n_casings=inputs['n_casings'], dro=inputs['dro'], dri=inputs['dri'],
                           dto=inputs['dto'], dti=inputs['dti'], wtg=inputs['wtg'], gt=inputs['gt'])

    return encode_utf8(html)


@app.route("/drilling")
def drilling():
    p, inputs = define_drill_plot()

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


if __name__ == "__main__":
    app.run(debug=True)

