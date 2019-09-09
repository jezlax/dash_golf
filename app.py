import dash
import dash_core_components as dcc
import dash_html_components as html
import flask
import dash_auth

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

app = dash.Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS)
server = app.server
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
app.config.suppress_callback_exceptions = True
