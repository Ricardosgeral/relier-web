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
server = app.server
app.title='relier web'

#connect to the data base

# cur= con.cursor() # as list
#
# try:
#     cur.execute("CREATE TABLE testdata ("
#                  "id serial PRIMARY KEY, "
#                  "date_time timestamp,"
#                  "duration interval, "
#                  "mmH2O_up integer, "
#                  "mmH2O_int integer, "
#                  "mmH2O_down integer, "
#                  "turb float, "
#                  "flow float, "
#                  "volume integer);")
#     con.commit()
# except:
#     cur.execute('rollback;')
#
# #create a table to parse test relevant inputs to  heroku app
# try:
#     cur.execute("CREATE TABLE testinputs (start timestamp, test_name varchar, rec_interval integer, test_type integer, "
#                 "mu float, bu float,mi float, bi float,md float, bd float,mturb float, bturb float);")
#     con.commit()
# except:
#     cur.execute('rollback;')


df_inputs = psql.read_sql('SELECT * FROM testinputs;', con)

#interval = (df_inputs['rec_interval'][0])*1000 # mseconds
interval = 8*1000
test_name = df_inputs['test_name'][0]
started = df_inputs['start'][0]
test_type = df_inputs['test_type'][0]

if test_type ==1:
    test_type_name = 'FLET'
elif test_type ==2:
    test_type_name = 'CFET'
elif test_type ==3:
    test_type_name = 'HET'
else:
    test_type_name = "Other"

###########################################
app.layout = html.Div([
    html.Div([
        html.H2("Sensor data streaming"),
        html.Img(src="https://raw.githubusercontent.com/Ricardosgeral/relier/master/Nextion/Illustrator/relier_dash-banner_.png"),
    ], className='banner'),

    html.Div([
        html.Div([
            html.H6("Name: {}  (Type: {})   ----> Started:  {:%Y-%m-%d, %H:%M} ".format(test_name, test_type_name, started)) # place filename and path of the csv file
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


@app.callback(Output('plots', 'figure'), [Input('data-update', 'n_intervals')])
def plots(interval):

    df = psql.read_sql('SELECT * FROM testdata;', con) # outputs


    x= df['duration'] = df['duration']/ np.timedelta64(1, 'm') # duration in minutes


    flow = Scatter(
        x=x,
        y=df['flow'],
        name='Flow rate ',
        mode='lines+markers',
        line=Line(color='blue', width= 1.5, shape='linear', dash = 'solid'),
        marker=Marker(color='blue', symbol='circle-open', opacity=0.7, size=6,
                      line=dict(width=1.5, color='blue')
                      ), #https://plot.ly/python/reference/#scatter-marker
        connectgaps = False,
        legendgroup = 'flowmeter',
    )

    volume = Scatter(
        x=x,
        y=df['volume'],
        name='Total volume',
        mode='lines',
        line=Line(color='green', width= 1.5, shape='linear', dash = 'solid'),
        connectgaps=False,
        fill='tozerox',
        fillcolor='lightgreen',
        yaxis='y2',
        legendgroup = 'flowmeter'
    )

    up_press = Scatter(
        x=x,
        y=df['mmh2o_up'],
        name='Ups pressure',
        mode='lines+markers',
        line=Line(color='blue', width= 1.5, shape='linear', dash = 'solid'),
        marker=Marker(color='blue', symbol='square-open', opacity=0.6, size=6,
                      line=dict(width=1.5, color='blue')
                      ),
        xaxis = 'x',
        yaxis='y3',
        legendgroup='pressures',
    )

    int_press = Scatter(
        x=x,
        y=df['mmh2o_int'],
        name='Int pressure',
        mode='lines+markers',
        line=Line(color='green', width= 1.5, shape='linear', dash = 'solid'),
        marker=Marker(color='green', symbol='square-open', opacity=0.6, size=6,
                      line=dict(width=1.5, color='green')
                      ),
        xaxis = 'x',
        yaxis='y3',
        legendgroup='pressures',
    )

    down_press = Scatter(
        x=x,
        y=df['mmh2o_down'],
        mode='lines+markers',
        line=Line(color='orange', width= 1.5, shape='linear', dash = 'solid'),
        marker=Marker(color='orange', symbol='square-open', opacity=0.6, size=6,
                      line=dict(width=1.5, color='orange')
                      ),
        name='Dwn pressure',
        xaxis='x',
        yaxis='y3',
        legendgroup='pressures',
    )

    turbidity = Scatter(
        x=x,
        y=df['turb'],
        mode='lines+markers',
        line=Line(color='blue', width=1.5, shape='linear', dash='solid'),
        marker=Marker(color='blue', symbol='diamond-open', opacity=0.6, size=6,
                      line=dict(width=1.5, color='blue')
                      ),
        name='Turbidity ',
        xaxis='x',
        yaxis='y4',
        legendgroup='turbiditymeter',
    )

    traces = [flow, volume, up_press, int_press, down_press, turbidity]

    layout = Layout(
        height=1000,
        #autosize=True,
        xaxis=dict(
            autorange=True,
            rangemode='nonnegative',
            #range=[0, max(df['duration'])],
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
            #side= 'top',
            #titlefont=dict(
                #family='Arial, sans-serif',
                #size=18,
                #color='lightgrey'
            #),
            mirror='allticks',

        ),
        yaxis=dict(
            autorange=True,
            #range=[min(df['flow']),max(df['flow'])],
            showgrid=True,
            ticks='inside',
            tickcolor='#adadad',
            tickwidth=2,
            showline=True,
            linecolor='#adadad',
            linewidth=2,
            fixedrange=False,
            zeroline=False,
            title='Flow rate (l/min)',
            domain =[0.72,1]
        ),
        yaxis2=dict(
            autorange=True,
            #range=[min(df['liters']), max(df['liters'])],
            showgrid=True,
            showline=True,
            linecolor='#adadad',
            linewidth=2,
            fixedrange=False,
            zeroline=False,
            title='Volume (l)',
            overlaying='y',
            side='right',
            ticks='inside',
            tickcolor='#adadad',
            tickwidth=2,
            mirror = 'allticks',
        ),
        yaxis3=dict(
            autorange=True,
            #range=[min(min(df['mmH2O_up']),min(df['mmH2O_int']),min(df['mmH2O_down'])),
            #       max(max(df['mmH2O_up']), max(df['mmH2O_int']), max(df['mmH2O_down']))],showgrid=False,
            showline=True,
            linecolor='#adadad',
            linewidth=2,
            fixedrange=False,
            zeroline=False,
            title='Piezometric pressure (mmH2O)',
            domain=[0.35, 0.63],
            ticks='inside',
            tickcolor='#adadad',
            tickwidth=2,
            mirror = 'allticks',

        ),
        yaxis4=dict(
            autorange=True,
           #range=[min(df['ntu_turb']),max(df['ntu_turb'])],
            showline=True,
            linecolor='#adadad',
            linewidth=2,
            fixedrange=False,
            zeroline=False,
            title='Turbidity (NTU)',
            domain = [0, 0.3],
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
            pad=2 # distance between graph and axis numbers
        ),
        legend = dict(x=0.05,y=5.5, orientation="h"),
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
    app.run_server(debug=True)