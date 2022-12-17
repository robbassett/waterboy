from flask import Flask, render_template, request
import config
from models import Plant
from plotting import plot_trace

app = config.connex_app
app.add_api(config.basedir / "swagger.yml")

@app.route("/plotting", methods=["POST", "GET"])
def make_plot():
    return plot_trace(request.args.get('data'))

@app.route("/")
def home():
    plants = Plant.query.all()
    return render_template("home.html", plants=plants)

@app.route("/dashboard/")
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)