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
    "Bianor fuses **data visualization** and **contextualization**.",
    "Train and observe the representation of high-dimensional datasets that are challenging to visualize otherwise — through Self-Organizing Maps (SOM) — revealing data topology to put complex observations in visual context.",
    "Visualize enhanced SOM displays, project historical patterns, and identify points of interest like anomalies directly from your Databricks catalog or from local data.",
]

layout = html.Div(
    children=[
        html.H3(title_header, className="mb-4"),
        dcc.Markdown(taglines[0]),
        dcc.Markdown(taglines[1]),
        dcc.Markdown(taglines[2]),
        html.Div(
            className="d-flex gap-3",
            style={"marginTop": "2rem", "flex-wrap": "wrap"},
            children=[
                dbc.Button([html.I(className="bi bi-map me-2"), "Explore Bianor"], color="primary",
                           size="md", href="/explorer"),
                dbc.Button([html.I(className="bi bi-github me-2"), "Get Started"], color="danger",
                           size="md", href="https://github.com/ophelia-rnd/bianor", target="_blank"),
                dbc.Button([html.I(className="bi bi-book me-2"), "Documentation"], outline=True, color="light",
                           size="md", href="https://bianor-documentation.onrender.com", target="_blank"),
                dbc.Button([html.I(className="bi bi-box-arrow-up-right me-2"), "About Bianor"], outline=True, color="secondary",
                           size="md", href="https://bianor.ophelia-rnd.dev", target="_blank"),
            ]
        )
    ]
)
