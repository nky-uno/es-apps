import dash_bootstrap_components as dbc
import dash_core_components as dcc
from retry import retry
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

def Navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("List", href="https://es-list.nky.uno")),
            dbc.NavItem(dbc.NavLink("Graph", href="https://es-graph.nky.uno")),
        ],
        brand="Nam KyungYim",
        brand_href="#",
        sticky="top",
    )
    return navbar
