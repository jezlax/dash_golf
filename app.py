import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, Event
import dash_bootstrap_components as dbc
import flask
import dash_auth
import os
from random import randint
import plotly.plotly as py
from plotly.graph_objs import *
import pandas as pd
from charts import *



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

#### CODE TO BUILD THE APP #### 

df = pd.read_csv('./assets/data.csv')
playerlist = df['PLAYER NAME'].unique().tolist()

def player_suggestions():
    return html.Datalist(
        id="player-list",
        children=[html.Option(value=word) for word in playerlist]
    )

def get_ids(playername):
    x = df[df['PLAYER NAME'] == '{}'.format(playername)]
    #print(x['id'].unique())
    return int(x['id'].unique()[0])



logo = [html.Img(src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Callaway_Golf_Company_logo.svg/1200px-Callaway_Golf_Company_logo.svg.png",
        style={"height":"100px"})]

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search",
                          placeholder="Choose Player",
                          id = 'choose-player',
                          autoComplete=True,
                          list='player-list')),
        dbc.Col(
            dbc.Button("Go!",
                       color="primary",
                       className="ml-2",
                       id = 'button'),
            width="auto",
        ),
    ],
    no_gutters=True,
    className="ml-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                    dbc.Col(dbc.NavbarBrand("Callaway Analytics", className="ml-2")),
                ],
                align="center",
                no_gutters=True,
            ),
            href="https://plot.ly",
        ),
        player_suggestions(),
        dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Collapse(search_bar, id="navbar-collapse", navbar=True),
    ],
    color="dark",
    dark=True,
)

body = html.Div(
            id = 'dashboard-div',
            style={"margin-top":"25px"},
            children=[
                #put the players' name and his slug in memory
                #dcc.Store(id='player-memory'),
                dcc.Store(id='memory'),


            #Row for Photo, Bio Info, and SG
          html.Div(
              className = "row mx-auto",
              style={"width":"100%", "height":"250px"},
              children=[
                    html.Div(
                        id = "photo-container",
                        className = "col-3",
                        style={"width":"100%","height":"100%", "padding-left":"50px"},
                        ),
                    html.Div(
                        id = "bio-container",
                        className = "col-3",
                        style={"width":"100%", "height":"100%"},
                    ),

                    html.Div(
                        id = 'sg-container',
                        className = "col-6",
                        style={"width":"100%", "height":"100%", "vertical-align":"top"},
                    )
              ]
          ),
          html.Div(
              className = "row mx-auto",
              style={"width":"100%", "height":"500px"},
              children=[
                    html.Div(
                        id = "line-container",
                        className = "col-7",
                        style={"width":"100%", "height":"100%"},
                    ),
                    html.Div(
                        id = "radar-container",
                        className = "col-5",
                        style={"width":"100%","height":"100%"},
                    )]
                )
        ])

### LOGO AND NAVBAR
header = html.Div(
    [
        dbc.Row(dbc.Col(logo)),
        dbc.Row(dbc.Col(navbar))
    ],
    style = {"width":"100%",
            "textAlign":"center",
            }
)

def layout():
    return html.Div(
            children=[
                html.Div(
                children=[header,body],
                style = {"width":"1300px",
                         "margin-left":"auto",
                         "margin-right":"auto",
                         "padding-top":"10px",
                         "background-color":"white"
                         },
                     )
            ],
            style = {"width":"100%",
                     "background-color":"grey"}
            )


##### CALL BACKS #####
#Add the Player ID to memory to callback for photo
@app.callback(
              Output("memory", "data"),
              [Input('button', 'n_clicks')],
              [State('choose-player', 'value'),]
              )
def get_player_ids_from_name(_,player):
    if player is None:
        return None
    else:
        return get_ids(player)

#PLAYER PHOTO CALLBACK
@app.callback(
    output=Output("photo-container","children"),
    inputs=[Input("memory", "modified_timestamp")],
    state=[State("memory","data")]
)
def slug_select(_,id):
    if id is None:
        return html.H2("Select a Player")
    else:
        return [html.Img(src="https://pga-tour-res.cloudinary.com/image/upload/c_fill,d_headshots_default.png,f_auto,g_face:center,h_350,q_auto,w_280/headshots_{}.png".format(id),
                         style={"height":"275px"})]

#GET BIO DATA
@app.callback(Output('bio-container', 'children'),
              [Input('button', 'n_clicks')],
              [State('choose-player', 'value'),]
              )
def callback_bio(_, selected_player):
    df = get_bio(selected_player)
    if selected_player is None:
        return None
    else:
        return [
            html.H2("{}".format(df['PLAYER NAME'].values.tolist()[0])),
            html.H6("{} Winnings: {}".format(df['SEASON'].values.tolist()[0],df['MONEY'].values.tolist()[0])),
            html.H6("{} Events: {}".format(df['SEASON'].values.tolist()[0],df['EVENTS'].values.tolist()[0])),
            html.H6("{} Victories: {}".format(df['SEASON'].values.tolist()[0],df['YTD VICTORIES'].values.tolist()[0]))
                ]

#STROKES GAINED DATA TABLE CALLBACK
@app.callback(
              Output('sg-container', "children"),
              [Input('button', 'n_clicks')],
              [State('choose-player', 'value'),]
              )
def callback_table(_,selected_player):
    if selected_player is None:
        return None
    else:
        return get_table(selected_player)

#LINE CHART CALLBACK
@app.callback(
              Output("line-container", "children"),
              [Input('button', 'n_clicks')],
              [State('choose-player', 'value'),]
              )
def callback_line(_,selected_player):
    if selected_player is None:
        return None
    else:
        return get_line(selected_player)

#RADAR CHART CALLBACK
@app.callback(
              Output("radar-container", "children"),
              [Input('button', 'n_clicks')],
              [State('choose-player', 'value'),]
              )

def callback_radar(_,selected_player):
    if selected_player is None:
        return None
    else:
        return get_radar(selected_player)

#### END OF THE APP CODE ####


# Run the Dash app
if __name__ == '__main__':
    app.layout = layout()
    app.server.run(debug=True, threaded=True)
    
