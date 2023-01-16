from flask import Flask, render_template, request
import config
from models import Plant
from plotting import get_trace
import os
from jinja2 import TemplateNotFound

app = config.connex_app
app.add_api(config.basedir / "swagger.yml") 

# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None

@app.route("/plotting", methods=["POST", "GET"])
def make_plot():
    return get_trace(request.args.get('data'))

@app.route("/")
def home():
    return render_template("/landing/index.html")

@app.route("/dashboard/")
def dashboard():
    plants = Plant.query.all()
    return render_template("/home/dashboard.html", plants=plants)

@app.route('/<template>')
def route_template(template):

    plants = Plant.query.all()
    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment, plants=plants)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)