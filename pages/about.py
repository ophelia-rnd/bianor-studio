import dash
import dash_bootstrap_components as dbc
from dash import html
import os

from registry import registry

dash.register_page(__name__, path="/about", title="About Bianor")

def layout():
    return dbc.Container(
        className="mt-5 text-white",
        children=[
            html.Div(
                className="p-4 rounded border border-secondary bg-dark shadow-sm",
                children=[
                    html.H4(registry.edition_name, className="text-primary mb-3"),
                    html.P([
                        html.Strong("Version: "), registry.version() if callable(registry.version) else registry.version
                    ]),
                    html.Hr(className="border-secondary my-4"),
                    registry.about_page_callout(),
                    html.Small("© 2026 Bianor. All rights reserved.", className="text-white-50")
                ]
            )
        ]
    )
