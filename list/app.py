import json
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from flask import Flask
import sys; sys.path.append('/opt/docker/pymodules')
import es_search
from navbar import Navbar
from dateselect import DateSelect

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Daily List'
server = app.server
 
navbar = Navbar()

body = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("Daily List"),
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
        return dbc.Table.from_dataframe(es_search.result('2020-01'), header={"1":"reading","2":"exercise","3":"coding","4":"english"}, striped=True, bordered=True)
    else:
        return dbc.Table.from_dataframe(es_search.result(value), header={"1":"reading","2":"exercise","3":"coding","4":"english"}, striped=True, bordered=True)

if __name__ == '__main__':
    app.run_server(debug=True)
