# app.py

from flask import Flask, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px

app = Flask(__name__)

@app.route('/callback', methods=['POST', 'GET'])
def cb():
    return gm(request.args.get('data'))

@app.route('/')
def index():
    return render_template('chartsajax.html', graphJSON=gm())

def gm(country='United Kingdom'):
    df = pd.DataFrame(px.data.gapminder())

    fig = px.line(df[df['country']==country], x="year", y="gdpPercap")

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)