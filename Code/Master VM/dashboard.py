import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Output, Input
import plotly
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from datetime import datetime

external_stylesheets = [dbc.themes.BOOTSTRAP, 'https://cdn.plot.ly/plotly-basic-2.12.1.min.js']
app = Dash(__name__, external_stylesheets=external_stylesheets)

params = ['Light_Level', 'Voltage', 'Temperature', 'Humidity', 'Solar_power', 'Estimated_demand', 'Conventional_power', 'Actual_demand']
df = pd.read_csv('dashboard_data.csv')

# Render the HTML Grid
app.layout = html.Div( # Div containing the Row-Col structure for the dashboard
        [
            html.Br(), # HTML tags in DBC
            dbc.Row([
                dbc.Col(dbc.Row([
                    html.B(id='time', style={'textAlign': 'end'}), html.I(children='Group 4', style={'textAlign': 'end'})
                ]), width=1),
                dbc.Col(html.H2(children="Hybrid Energy inspired DC Microgrid System using Machine Learning", style={'textAlign': 'center'}), width=11)
            ]),
            dbc.Row([html.Br()]),
            dbc.Row( # This is the stucture using placeholders for each graph component, identified with an id, the actual graph code is defined below.
                [
                    dbc.Col(dcc.Graph(id='Light_Level', animate=True), width=3), # Graph components(defined below) in Columns
                    dbc.Col(dcc.Graph(id='Voltage', animate=True), width=3), # Bootstrap screen width = 12 row units
                    dbc.Col(dcc.Graph(id='Temperature', animate=True), width=3),
                    dbc.Col(dcc.Graph(id='Humidity', animate=True), width=3)
                ],
                className="g-0", # Remove gutter (horizontal padding)
            ),

            dbc.Row(
                [
                    dbc.Col([dcc.Graph(id='Total_Power', animate=True)], width=6),
                    dbc.Col([dcc.Graph(id='Load_Comparison', animate=True)], width=6),
                ],
                className="g-0",
            ),
            dcc.Interval(
                id='interval-component',
                interval=1000, # milliseconds - Reload the graphs after 5 seconds
            )
        ],
    )

# A decorator for the time component of the dashboard - uses the defined inteval as the input and outputs time to the children attribute of html component having id = time.
@app.callback([Output('time','children')], [Input('interval-component', 'n_intervals')])
def show_time(n):
    # Show Current Time
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return [current_time]

# Update the graph component, having id = Light_Level's figure attribute
@app.callback([Output('Light_Level','figure')], [Input('interval-component', 'n_intervals')])
def g1(n):
    global df 

    # Read d.csv into a dataframe (updated every 5 seconds as per set interval)
    df = pd.read_csv('dashboard_data.csv')

    # Plot Light_Level vs Time graph for the updated dataframe 
    data = []
    trace = go.Scatter(x=df.index, y=df['Light_Level'].tolist(), marker=dict(color='orange'), mode='lines+markers')
    data.append(trace)

    # Draw the graph component and return it
    layout = go.Layout(xaxis={'title': 'Time'}, yaxis={'title': 'Light Level (lux)'}, width=300, height=200, showlegend=False, margin=dict(r=0, t=10, b=10))
    figure = go.Figure(data=data, layout=layout)
    return [figure]

# Similarly, 3 other features are plotted vs Time

@app.callback([Output('Voltage','figure')], [Input('interval-component', 'n_intervals')])
def g2(n):
    global df 
    data = []
    trace = go.Scatter(x=df.index, y=df['Voltage'].tolist(), marker=dict(color='red'), mode='lines+markers')
    data.append(trace)
    layout = go.Layout(xaxis={'title': 'Time'}, yaxis={'title': 'PV Panel Voltage (V)'}, width=300, height=200, showlegend=False, margin=dict(r=0, t=10, b=10))
    figure = go.Figure(data=data, layout=layout)
    return [figure]

@app.callback([Output('Temperature','figure')], [Input('interval-component', 'n_intervals')])
def g3(n):
    global df 
    data = []
    trace = go.Scatter(x=df.index, y=df['Temperature'].tolist(), marker=dict(color='green'), mode='lines+markers')
    data.append(trace)
    layout = go.Layout(xaxis={'title': 'Time'}, yaxis={'title': 'Temperature (°C)'}, width=300, height=200, showlegend=False, margin=dict(r=0, t=10, b=10))
    figure = go.Figure(data=data, layout=layout)
    return [figure]

@app.callback([Output('Humidity','figure')], [Input('interval-component', 'n_intervals')])
def g4(n):
    global df 
    data = []
    trace = go.Scatter(x=df.index, y=df['Humidity'].tolist(), marker=dict(color='blue'), mode='lines+markers')
    data.append(trace)
    layout = go.Layout(xaxis={'title': 'Time'}, yaxis={'title': 'Humidity (%)'}, width=300, height=200, showlegend=False, margin=dict(r=0, t=10, b=10))
    figure = go.Figure(data=data, layout=layout)
    return [figure]

@app.callback([Output('Total_Power','figure')], [Input('interval-component', 'n_intervals')])
def g5(n):
    global df
    labels = ['Solar Power', 'Conventional Power']
    values = [df['Solar_power'].iloc[-1], df['Conventional_power'].iloc[-1]]
    trace = go.Pie(labels=labels, values=values, hole=0.5, textinfo='value', insidetextfont={'color': 'white'}, texttemplate='%{value:.3f}')
    layout = go.Layout(title='Power Plant Generation (W)')
    figure = go.Figure(data=[trace], layout=layout)
    return [figure]

@app.callback([Output('Load_Comparison','figure')], [Input('interval-component', 'n_intervals')])
def g6(n):
    global df
    figure = go.Figure()
    figure.add_bar(x=df.index, y=df['Estimated_demand'], name='Estimated Load', base=0, marker=dict(color='purple'))
    figure.add_bar(x=df.index, y=df['Actual_demand'], name='Actual Load', base=0, marker=dict(color='magenta'))    

    figure.update_layout(
        title='Power Plant Generation',
        xaxis=dict(title='Time'),
        yaxis=dict(title='Power Generation (V)'),
    )
    return [figure]

# Run the Dash app on localhost

if __name__ == "__main__":
    app.run_server(host= '0.0.0.0', debug=False)
