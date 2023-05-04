from flask import Flask, render_template, request
import config
from models import Plant
from plotting import output_plotly,get_trace
from image import upload_image
from profile import get_profile_info
from jinja2 import TemplateNotFound
import numpy as np

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

@app.route("/plotting", methods=["GET"])
def make_plot():
    return output_plotly(request.args.get('data'))

@app.route("/profile",methods=["GET"])
def get_profile():
    return get_profile_info(request.args.get('data'))

@app.route("/")
def home():
    return render_template("/landing/index.html")

@app.route("/dashboard/")
def dashboard():
    plants = Plant.query.all()
    water = []
    light = []
    for plant in plants: 
        try:
            t = get_trace(plant.plant_name).split('], [')
            t1 = str(np.around(float(t[0][:-1].split(',')[-1]),1))
            t2 = str(np.around(float(t[1][:-2].split(',')[-1]),1))
        except:
            t1,t2 = '10.0','10.0'
        water.append(t1)
        light.append(t2)
    return render_template("/home/dashboard.html", plants=plants, water=water, light=light)

@app.route('/<template>')
def route_template(template):

    plants = Plant.query.all()
    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)
        water,light = [],[]
        for plant in plants: 
            try:
                t = get_trace(plant.plant_name).split('], [')
                t1 = np.around(float(t[0][:-1].split(',')[-1]),1)
                t2 = np.around(float(t[1][:-2].split(',')[-1]),1)
            except:
                t1,t2 = 10.0,10.0
            water.append(t1)
            light.append(t2)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment, plants=plants, water=water, light=light)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)