import time
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from flask import Flask
import sys; sys.path.append('/opt/docker/pymodules')
import es_search
from navbar import Navbar
from dateselect import DateSelect

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Daily Graph'
server = app.server

navbar = Navbar()
body = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("Daily Graph"),
                        html.P(
                            """\
The lifestyle is recorded.
Recordkeeping uses elasticsearch.
made with python and flask.
It is based on docker container."""
                        ),
                    ],
                    md=3,
                ),
                dbc.Col(
                    [
                        DateSelect(),
                        html.Div(id='date-display-value')
                    ]
                ),
            ]
        )
    ],
    className="mt-4",
)

app.layout = html.Div([navbar, body])

@app.callback(
    Output('date-display-value', 'children'),
    [Input('date-dropdown', 'value')])
def display_value(value):
    if value is None:
        df = es_search.result(time.strftime("%Y-%m"))
    else:
        df = es_search.result(value)
    graph = dcc.Graph(
                figure={
                    'data': [go.Scatter(x=df["date"],y=df["1"],name="reading",mode="lines+markers"),
                             go.Scatter(x=df["date"],y=df["2"],name="exercise",mode="lines+markers"),
                             go.Scatter(x=df["date"],y=df["3"],name="coding",mode="lines+markers"),
                             go.Scatter(x=df["date"],y=df["4"],name="english",mode="lines+markers")],
                    'layout':{'xaxis':{'tickformat':'%Y/%m/%d'}}
                }
            ),
    return graph

if __name__ == '__main__':
    app.run_server(debug=True)
