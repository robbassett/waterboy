from flask import Flask, render_template
import config
from models import Plant

app = config.connex_app
app.add_api(config.basedir / "swagger.yml")

@app.route("/")
def home():
    plants = Plant.query.all()
    return render_template("home.html", plants=plants)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)