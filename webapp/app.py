#! /usr/bin/python3.6
# -*- coding: utf-8 -*-
#Ricardos.geral@gmail.com
#Visualization of sensor data from relier acquisition system using Dash/Plotly on Heroku
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from plotly.graph_objs import *
import numpy as np
import pandas.io.sql as psql
import psycopg2 as p
import urllib.parse as urlparse
import os

url = urlparse.urlparse(os.environ['DATABASE_URL'])
dbname = url.path[1:]
user = url.username
password = url.password
host = url.hostname
port = url.port

con = p.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
            )

app = dash.Dash()
app.title='Relier web stream'

interval = 5*1000


@app.callback(Output('plots', 'figure'), [Input('data-update', 'n_intervals')])
def plots(interval):

    df_inputs = psql.read_sql('SELECT * FROM testinputs ORDER BY test_name;', con)
    df = psql.read_sql('SELECT * FROM testdata ORDER BY id;', con) # outputs

    test_name = df_inputs['test_name'][0]
    started = df_inputs['start'][0]
    test_type = df_inputs['test_type'][0]

    if test_type == 1:
        test_type_name = 'FLET'
    elif test_type == 2:
        test_type_name = 'CFET'
    elif test_type == 3:
        test_type_name = 'HET'
    else:
        test_type_name = "Other"

    ###########################################
    app.layout = html.Div([
        html.Div([
            html.H2("Sensor data streaming"),
            html.Img(
                src="https://raw.githubusercontent.com/Ricardosgeral/relier/master/Nextion/Illustrator/relier_dash-banner_.png"),
        ], className='banner'),

        html.Div([
            html.Div([
                html.H6("Name: {}  (Type: {})   ----> Started:  {:%Y-%m-%d, %H:%M} ".format(test_name, test_type_name,
                                                                                            started))
                # place filename and path of the csv file
            ], className='row'),
        ], className='row wind-speed-row'),

        html.Div([
            html.Div([
                html.H3("Plots")
            ], className='Title'),
            html.Div([
                dcc.Graph(id='plots'),
            ], className='row'),

            dcc.Interval(id='data-update', interval=interval, n_intervals=0),
        ], className='row wind-speed-row'),
    ],
        style={'padding': '0px 10px 15px 10px',
               'marginLeft': 'auto', 'marginRight': 'auto', "width": "900px",
               'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'})

    flow = Scatter(
        y=df['flow'],
        x=df['duration']/ np.timedelta64(1, 'm'),
        name='Flow rate ',
        mode='lines+markers',
        line=Line(color='green', width= 2.0, shape='linear', dash = 'solid'),
        marker=Marker(color='green', symbol='circle-open', opacity=0.7, size=6.5,
                      line=dict(width=1.5, color='green')
                      ), #https://plot.ly/python/reference/#scatter-marker
        connectgaps = False,
        legendgroup = 'flowmeter',
        yaxis='y2',

    )

    volume = Scatter(
        x=df['duration'] / np.timedelta64(1, 'm'),
        y=df['volume'],
        name='Total volume',
        mode='lines',
        opacity = 0.5,
        line=Line(color='blue', width=1.5, shape='linear', dash='solid'),
        connectgaps=False,
        fill='tonexty',
        fillcolor='#f4fbff',
        legendgroup='flowmeter',

    )


    up_press = Scatter(
        x=df['duration']/ np.timedelta64(1, 'm'),
        y=df['mmh2o_up'],
        name='Ups pressure',
        mode='lines+markers',
        line=Line(color='blue', width= 1.5, shape='linear', dash = 'solid'),
        marker=Marker(color='blue', symbol='square-open', opacity=0.6, size=6.5,
                      line=dict(width=1.5, color='blue')
                      ),
        xaxis = 'x',
        yaxis='y3',
        legendgroup='pressures',
    )

    int_press = Scatter(
        x=df['duration']/ np.timedelta64(1, 'm'),
        y=df['mmh2o_int'],
        name='Int pressure',
        mode='lines+markers',
        line=Line(color='green', width= 1.5, shape='linear', dash = 'solid'),
        marker=Marker(color='green', symbol='square-open', opacity=0.6, size=6.5,
                      line=dict(width=1.5, color='green')
                      ),
        xaxis = 'x',
        yaxis='y3',
        legendgroup='pressures',
    )

    down_press = Scatter(
        x=df['duration']/ np.timedelta64(1, 'm'),
        y=df['mmh2o_down'],
        mode='lines+markers',
        line=Line(color='orange', width= 1.5, shape='linear', dash = 'solid'),
        marker=Marker(color='orange', symbol='square-open', opacity=0.6, size=6.5,
                      line=dict(width=1.5, color='orange')
                      ),
        name='Dwn pressure',
        xaxis='x',
        yaxis='y3',
        legendgroup='pressures',
    )

    turbidity = Scatter(
        x=df['duration']/ np.timedelta64(1, 'm'),
        y=df['turb'],
        mode='lines+markers',
        line=Line(color='blue', width=1.5, shape='linear', dash='solid'),
        marker=Marker(color='blue', symbol='diamond-open', opacity=0.6, size=6.5,
                      line=dict(width=1.5, color='blue')
                      ),
        name='Turbidity',
        xaxis='x',
        yaxis='y4',
        legendgroup='turbidity_meter',
    )

    traces = [flow, volume, down_press, int_press, up_press, turbidity]

    layout = Layout(
        height=1200,
        xaxis=dict(
            autorange=True,
            rangemode='nonnegative',
            showgrid=True,
            showline=True,
            linecolor='#adadad',
            linewidth=2,
            zeroline=False,
            zerolinewidth=2,
            fixedrange=False,
            autotick=True,
            ticks='inside',
            tick0=0,
            dtick=1,
            ticklen=8,
            tickwidth=2,
            tickcolor='#adadad',
            showticklabels=True,
            title='Duration (min)',
            showaxeslabels=True,
            side= 'top',
            #titlefont=dict(
                #family='Arial, sans-serif',
                #size=18,
                #color='lightgrey'
            #),
            mirror='allticks',

        ),
        yaxis=dict(
            autorange=True,
            rangemode='nonnegative',
            showgrid=True,
            ticks='inside',
            tickcolor='#adadad',
            tickwidth=2,
            showline=True,
            linecolor='#adadad',
            linewidth=2,
            fixedrange=False,
            zeroline=True,
            title='Volume (liters)',
            domain =[0.657,0.96],
            side = 'right'


        ),
        yaxis2=dict(
            autorange=True,
            rangemode='nonnegative',
            showgrid=True,
            showline=True,
            linecolor='#adadad',
            linewidth=2,
            fixedrange=False,
            zeroline=False,
            title='Flow rate (liters/min)',
            overlaying='y',
            side='left',
            ticks='inside',
            tickcolor='#adadad',
            tickwidth=2,
            mirror = 'False',

        ),
        yaxis3=dict(
            autorange=True,
            showline=True,
            linecolor='#adadad',
            linewidth=2,
            fixedrange=False,
            zeroline=False,
            title='Piezometric pressure (mmH2O)',
            domain=[0.328, 0.632],
            ticks='inside',
            tickcolor='#adadad',
            tickwidth=2,
            mirror = 'allticks',

        ),
        yaxis4=dict(
            autorange=True,
            showline=True,
            linecolor='#adadad',
            linewidth=2,
            fixedrange=False,
            zeroline=False,
            title='Turbidity (NTU)',
            domain = [0, 0.303],
            ticks='inside',
            tickcolor='#adadad',
            tickwidth=2,
            mirror='allticks',

    ),
        margin=Margin(
            t=50,
            l=60,
            r=60,
            b=20,
            pad=1.5 # distance between graph and axis numbers
        ),
        legend = dict(x=-0.08, y=1.075, orientation="h"),
        #paper_bgcolor='#7f7f7f',
        #plot_bgcolor='#f6f6f6',
    )

    return Figure(data=traces, layout=layout)


external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/737dc4ab11f7a1a8d6b5645d26f69133d97062ae/dash-wind-streaming.css",
                "https://fonts.googleapis.com/css?family=Raleway:400,400i,700,700i",
                "https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i"]

for css in external_css:
    app.css.append_css({"external_url": css})

if 'DYNO' in os.environ:
    app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'
})

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=os.environ.get('PORT'))