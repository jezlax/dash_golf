import pandas as pd
import numpy as np
from plotly import graph_objects as go
import pandas as pd
import plotly.figure_factory as ff
import dash_core_components as dcc

df = pd.read_csv('./assets/data.csv')

def get_bio(playername):
    current = df[(df['SEASON'] == 2019) & (df['PLAYER NAME'] == '{}'.format(playername))]
    current['MONEY'] = df['MONEY'].map('${:,.0f}'.format)
    final = current[['PLAYER NAME','SEASON','EVENTS','MONEY','YTD VICTORIES']]
    return final

def get_table(playername):
    current = df[(df['SEASON'] == 2019) & (df['PLAYER NAME'] == '{}'.format(playername))]
    cats = ['Off The Tee','Approach','Around The Green','Putting']
    ott = current['SG:OTT'].values.tolist()[0]
    app = current['SG:APP'].values.tolist()[0]
    atg = current['SG:ATG'].values.tolist()[0]
    putt = current['SG:PUTT'].values.tolist()[0]

    ottrk = current['sg_ott_rk'].values.tolist()[0]
    apprk = current['sg_app_rk'].values.tolist()[0]
    atgrk = current['sg_atg_rk'].values.tolist()[0]
    puttrk = current['sg_putt_rk'].values.tolist()[0]

    rowEvenColor = 'lightgrey'
    rowOddColor = 'white'

    fig = go.Figure(data=[go.Table(
    columnwidth=[20,20,20],
    header=dict(values=['Category','SG','Rank'],
                fill_color='darkblue',
                font=dict(color='white',size=18),
                align=['left','center']),
    cells=dict(values=[cats,[ott,app,atg,putt],[ottrk,apprk,atgrk,puttrk]],
               fill_color = [[rowOddColor,rowEvenColor,rowOddColor, rowEvenColor]*3],
               align=['left','center'],
               font=dict(size=16),
               height=30))
               ])
    fig.update_layout(title = '<b>2019 Strokes Gained Data</b>',
                      title_x = 0.5,
                      title_y = 0.99,
                      height = 350,
                      margin={"t":20,"b":0,"l":0,"r":0}
                      )
    return dcc.Graph(figure=fig, style={"height": "100%", "width": "100%"})

def get_radar(playername):
    x = df[(df['PLAYER NAME'] == playername) & (df['SEASON']==2019)]
    y = df[(df['PLAYER NAME'] == playername) & (df['SEASON']==2018)]
    cy = x[['sg_ott_pctle','sg_app_pctle','sg_atg_pctle','sg_putt_pctle']].values.tolist()[0]
    py = y[['sg_ott_pctle','sg_app_pctle','sg_atg_pctle','sg_putt_pctle']].values.tolist()[0]
    categories = ['Off The Tee','Approach','ATG','Putting']

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
      r=cy,
      theta=categories,
      fill='toself',
      name='2019'
    ))
    fig.add_trace(go.Scatterpolar(
          r=py,
          theta=categories,
          fill='toself',
          name='2018'
    ))

    fig.update_layout(
      polar=dict(
        radialaxis=dict(
          visible=True,
          range=[0,100]
        ),
      ),
      showlegend=True
    )
    fig.update_layout(title = '<b>2019 Strokes Gained Data</b><br> Percentile Rank </br>',
                      title_x = 0.5,
                      width=500,
                      margin={"t":30,"b":0,"l":30,"r":0})
    return dcc.Graph(figure=fig, style={"height": "100%", "width": "100%"})


#LINECHART
def get_line(playername):
    x = df[(df['PLAYER NAME'] == playername)]
    title = 'Strokes Gained by Season'
    labels = ['OFF','APP','ATG','PUTT']
    colors = ['rgb(67,67,67)', 'rgb(115,115,115)', 'rgb(49,130,189)', 'rgb(189,189,189)']

    ottrk = x['sg_ott_rk'].values.tolist()
    apprk = x['sg_app_rk'].values.tolist()
    atgrk = x['sg_atg_rk'].values.tolist()
    puttrk = x['sg_putt_rk'].values.tolist()

    x_data = np.vstack((np.arange(x['SEASON'].min(),x['SEASON'].max()+1),)*4)
    #x_data = [df['SEASON'].values.tolist()]*4
    vals = [ottrk,apprk,atgrk,puttrk]

    fig = go.Figure()

    for i in range(0, 4):
        fig.add_trace(go.Scatter(x=x_data[i], y=vals[i], mode='lines',
            name=labels[i],
            line=dict(color=colors[i], width=4),
            connectgaps=True,
        ))

    fig.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=False,
            autorange='reversed'
        ),
        autosize=False,
        margin=dict(
            autoexpand=False,
            l=100,
            r=20,
            t=110,
        ),
        showlegend=False,
        plot_bgcolor='white',
        #width=550
    )

    annotations = []

    # Adding labels
    for y_trace, label, color in zip(vals, labels, colors):
    # labeling the left_side of the plot
        annotations.append(dict(xref='paper', x=0, y=y_trace[0],
                                      xanchor='right', yanchor='middle',
                                      text=label + ' {}'.format(y_trace[0]),
                                      font=dict(family='Arial',
                                                size=14),
                                      showarrow=False))
        # labeling the right_side of the plot
        annotations.append(dict(xref='paper', x=1.0, y=y_trace[-1], #this needs to be the last element in the list
                                      xanchor='left', yanchor='middle',
                                      text='{}'.format(y_trace[-1]),
                                      font=dict(family='Arial',
                                                size=14),
                                      showarrow=False))
        # Title
        annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                                      xanchor='left', yanchor='bottom',
                                      text='Strokes Gained by Season',
                                      font=dict(family='Arial',
                                                size=24,
                                                color='rgb(37,37,37)'),
                                      showarrow=False))
        # Source
        annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                                      xanchor='center', yanchor='top',
                                      text='Season',
                                      font=dict(family='Arial',
                                                size=12,
                                                color='rgb(150,150,150)'),
                                      showarrow=False))

    fig.update_layout(annotations=annotations)



    return dcc.Graph(figure=fig, style={"height": "100%", "width": "100%"})
