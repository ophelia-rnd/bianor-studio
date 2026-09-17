import dash
import dash_bootstrap_components as dbc

from dash import html, dcc

dash.register_page(
    __name__,
    path="/",
    name="Home",
    icon="bi-house-door"
)

title_header = "Welcome to Bianor"
taglines = [
    "Bianor fuses **data visualization** and **contextualization** with **anomaly detection**.",
    "Visualize enhanced Self-Organizing Maps (SOM), project historical patterns, and identify points of interest like anomalies directly from your Databricks catalog."
]

layout = html.Div(
    children=[
        html.H3(title_header, className="mb-4"),
        dcc.Markdown(taglines[0]),
        dcc.Markdown(taglines[1]),
        html.Div(
            className="d-flex gap-3",
            style={"marginTop": "2rem", "flex-wrap": "wrap"},
            children=[
                dbc.Button([html.I(className="bi bi-map me-2"), "Explore Bianor"], color="primary",
                           size="md", href="/explorer"),
                dbc.Button([html.I(className="bi bi-github me-2"), "Install in Databricks"], outline=True, color="danger",
                           size="md", href="https://github.com/ophelia-rnd/bianor-databricks", target="_blank"),
                dbc.Button([html.I(className="bi bi-box-arrow-up-right me-2"), "About Bianor"], outline=True, color="secondary",
                           size="md", href="https://bianor.ophelia-rnd.dev", target="_blank"),
                dbc.Button([html.I(className="bi bi-linkedin me-2"), "Team behind Bianor"], outline=True, color="info",
                           size="md", href="https://linkedin.com/company/ophelia-rnd", target="_blank"),
            ]
        )
    ]
)
