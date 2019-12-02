from flask import Flask, render_template, request, redirect
import pwptemp.drilling as ptd

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "POST":
        time = int(request.form.get("time"))
        depth = int(request.form.get("depth"))
        wd = request.form.get("wd")
        well_profile = request.form.get("well_profile")

        ptd.temp(time, mdt=depth).plot()

        return redirect(request.url)

    return render_template("profile.html")


if __name__ == "__main__":
    app.run(debug=True)

