import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, Event
import flask
import dash_auth
import os
from random import randint
import plotly.plotly as py
from plotly.graph_objs import *




# import pandas as pd
EXTERNAL_STYLESHEETS = [
    {
        "href": "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css",
        "rel": "stylesheet",
        "integrity": "sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T",
        "crossorigin": "anonymous",
    }
]

VALID_USERNAME_PASSWORD_PAIRS = {
    'callaway': 'epic'
}


# Setup the app
# Make sure not to change this file name or the variable names below,
# the template is configured to execute 'server' on 'app.py'

server = flask.Flask(__name__)
server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))

app = dash.Dash(__name__, server=server external_stylesheets=EXTERNAL_STYLESHEETS)
server = app.server
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
app.config.suppress_callback_exceptions = True




# Put your Dash code here


# Run the Dash app
if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)
